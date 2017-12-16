'use strict';

const AWS = require('aws-sdk');
const SES = new AWS.SES({ region: 'eu-west-1' });
const MAX_TEMPERATURE = parseFloat(45);
const MIN_TEMPERATURE = parseFloat(10);
const MAX_HUMIDITY = parseFloat(70);
const MIN_HUMIDITY = parseFloat(20);

function sendEmail(sensor_name, datetime, temperature, humidity, alerts) {
    const body = "Sensor: " + sensor_name + ". "
        + "Date Time: " + datetime + ". "
        + "Temperature: " + temperature + ". "
        + "Humidity: " + humidity + ". "
        + "Alerts: " + alerts.join(", ");
        
    console.log(body);
    
    const eParams = {
        Destination: {
            ToAddresses: ["albert.moreno.dev@gmail.com"]
        },
        Message: {
            Body: {
                Text: { Data: body }
            },
            Subject: { Data: "[Alarm] Temp & Humidity" }
        },
        Source: "albert.moreno.dev@gmail.com"
    };

    SES.sendEmail(eParams, function(err, data){
        if(err) console.log(err);
    });
}

function searchAlerts(temperature, humidity) {
    var alerts = [];
    
    if (temperature > MAX_TEMPERATURE) {
        alerts.push('Maximum of temperature reached');
    } else if (temperature < MIN_TEMPERATURE) {
        alerts.push('Minimum of temperature reached');
    }
    
    if (humidity > MAX_HUMIDITY) {
        alerts.push('Maximum of humidity reached');
    } else if (humidity < MIN_HUMIDITY) {
        alerts.push('Minimum of humidity reached');
    }
    
    return alerts;
}

exports.handler = (event, context, callback) => {
    const message = event.Records[0].Sns.Message;
    const parsedMessage = JSON.parse(message);
    const sensor_name = parsedMessage.sensor_name;
    const datetime = parsedMessage.datetime;
    const temperature = parseFloat(parsedMessage.temperature);
    const humidity = parseFloat(parsedMessage.humidity);
    
    const alerts = searchAlerts(temperature, humidity);
    
    if (alerts.length > 0) {
        sendEmail(sensor_name, 
            datetime,
            temperature,
            humidity,
            alerts);
    }
    
    console.log('From SNS:', parsedMessage);
    callback(null, message);
};
