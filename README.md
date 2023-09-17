# WhatsApp Chat Analyser

This Project is made to analyse a whatsapp chats and see the statistics of the chats.

The Projects Shows following Features :
1. Overall Statistics 
1. Top Chatist Users (Only for Overall Analysis)
1. Word Cloud
1. Most Common Words
1. Emojis
1. Activity Graph
1. Timeline
1. Hourly Activity

## :radioactive: Caution

### Date and Time Format
The Uploaded file should be in **24 Hours** Format. 

For Convertning the format : Just Change the Date Time of your Device and Then Export The Chat.

### Media
Extract it **Without Media**. When You will click on extract it will show an option there You will get the option. 

This Shall generate a ***.txt***  file and upload that file here for the analysis.

## Running

To Run this Code just Follow the given steps :

### Fork and Star
Before You run the code you need to *Fork and Star* this repo. For this just click on the options seen in the top of the Repo.

### Clone
Get this code in your system using the git. Make sure that ***git*** is installed in your system.

After that run the following commad :
```shell
git clone https://github.com/your_username_/WhatsApp_Chat_Analyser.git
```

### Change the location
Now change th directory 
```shell
cd WhatsApp_Chat_Analyser
```

### Installing the dependencies
This command can take time to complete depending on you internet connections.

This is required for downloading the module on which the code depeneds and this is one of the most important step.
```shell
pip install -r requirements.txt
```

### Locally Hosting 
Now you are in the required directory and now you need to run the streamlit app. For this run the below command :

```shell
streamlit run app.py
```
<br>
Now the webpage will open in the Default browser and you would be able to use this.

Uplaod the extracted Chat and you can see the Analysis of the Chats.
This could be seen in 2 phases 

- **Overall** : For all the users in the chat
- **Individual Level** : For this Just select the user and click on analyse button.


## :technologist: Technologies and Modules

### Streamlit
Used this to make the webpage to create the web page to read the chats and Show the outputs.

### MatplotLib and SeaBorn
These are the Basic requirements for the Creating the Graphs. All the Graphs are created using these 2 libraries only.

### Numpy and Pandas
Another Basic Requirements for the analysing things. These are also used for making DataFrames that are shown in the webpage.

### Word Cloud
Used this to show the Words used in the graph.

### Emojis
These is used to work on the Emojis. As the Emojis can not be directly analysed in python.

### URLextractor and RegEx
Url extractor was needed to get all the links present in the Chats. RegEx is an Important thing for splitting the string and get the required info.
