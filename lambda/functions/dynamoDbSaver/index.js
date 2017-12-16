'use strict';

const AWS = require('aws-sdk');
const SES = new AWS.SES({ region: 'eu-west-1' });
const SQS = new AWS.SQS({ apiVersion: '2012-11-05' });
const Lambda = new AWS.Lambda({ apiVersion: '2015-03-31' });
const DynamoDB = new AWS.DynamoDB.DocumentClient({region: 'eu-west-1'});
const uuid = require('node-uuid');

// Your queue URL stored in the queueUrl environment variable
const QUEUE_URL = process.env.queueUrl;
const PROCESS_MESSAGE = 'process-message';
const TABLE_NAME = 'tempAndHumidity';

function invokePoller(functionName, message) {
    console.log('invokePoller', functionName, message.Body);
    const payload = {
        operation: PROCESS_MESSAGE,
        message,
    };
    const params = {
        FunctionName: functionName,
        InvocationType: 'Event',
        Payload: new Buffer(JSON.stringify(payload)),
    };
    return new Promise((resolve, reject) => {
        Lambda.invoke(params, (err) => (err ? reject(err) : resolve()));
    });
}


function processMessage(message, callback) {
    console.log('processMessage', message.Body);

    const promise = storeData(message.Body)
    .then((result) => {
        console.log("Success:", result);
        
        // delete message
        const params = {
            QueueUrl: QUEUE_URL,
            ReceiptHandle: message.ReceiptHandle,
        };
        SQS.deleteMessage(params, (err) => callback(err, message));
    })
    .catch((err) => {
        console.log("Error: ", err);
    });
}

function storeData(messageBody) {
    var parsedMessageBody = JSON.parse(messageBody);
    var params = {
		Item: {
		    id: uuid.v4(),
            date: Date.now() / 1000 | 0,
            recorded_datetime: new Date(parsedMessageBody.datetime).getTime() / 1000 | 0,
            sensor_name: parsedMessageBody.sensor_name,
            temperature: parseFloat(parsedMessageBody.temperature),
            humidity: parseFloat(parsedMessageBody.humidity)
		},
		TableName: TABLE_NAME
	};
	
	console.log('storeData', params);
	
	return new Promise((resolve, reject) => {
        DynamoDB.put(params, (err, data) => (err ? reject(err) : resolve()));
    });
}

function poll(functionName, callback) {
    console.log('poll', functionName);
    const params = {
        QueueUrl: QUEUE_URL,
        MaxNumberOfMessages: process.env.MaxNumberOfMessages,
        VisibilityTimeout: 10,
    };
    // batch request messages
    SQS.receiveMessage(params, (err, data) => {
        if (err) {
            return callback(err);
        }
        // for each message, reinvoke the function
        const promises = data.Messages.map((message) => invokePoller(functionName, message));
        // complete when all invocations have been made
        Promise.all(promises).then(() => {
            const result = `Messages received: ${data.Messages.length}`;
            console.log(result);
            
            callback(null, result);
        });
    });
}

function sendEmail(message) {
    var eParams = {
        Destination: {
            ToAddresses: ["albert.moreno.dev@gmail.com"]
        },
        Message: {
            Body: {
                Text: { Data: message }
            },
            Subject: { Data: "Temp & Humidity" }
        },
        Source: "albert.moreno.dev@gmail.com"
    };

    var email = SES.sendEmail(eParams, function(err, data){
        if(err) console.log(err);
    });
}

exports.handler = (event, context, callback) => {
    try {
        if (event.operation === PROCESS_MESSAGE) {
            // invoked by poller
            processMessage(event.message, callback);
        } else {
            // invoked by schedule
            poll(context.functionName, callback);
        }
    } catch (err) {
        callback(err);
    }
};
