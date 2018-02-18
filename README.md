# Zack Khan Handshake Alarm Project

## Components of the Application: 
- MongoDB Database that stores a Alarm Schema (holds time, name, and number of votes of alarm) 
- Webpage where user enters the name and time of alarm (time is validated). Sound (using Howler.js) and popup appear when an alarm rings
- Node.js Backend 

## Assumptions: 
- It would be easier for user to enter the time vs selecting time via dropdown 
- Using Military Time for international use (in future I would add a toggle feature to switch)
- Alarms are always made for the current day

## Prioritization
Core Functionality first due to strict time limits

## Test Cases Covered
-Inputting invalid number (ex: entering 13 for month) returns an Internal Error response and does not create an alarm 
-Checking that if multiple users access the app, all users see an alarm ring 

## How to Run
Go to: 165.227.220.148
(Hosted on Digital Ocean) 
