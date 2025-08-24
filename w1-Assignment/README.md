# W1 Assignment - Text Analysis Tool

## Prerequisites
Please install all the libraries in the requirement.txt

## Project Details
This project feature a summarization feature that can summarize any type of long-form input that you give to it. Additionally, it also features a tokenization explorer that helps you understand just how many tokens the prompt you use contains. In addition to these primary feature, the project also features a language detector and a results exporter. The language detector scans through the prompt and tells what the language is based on the highest probability. This is all done by the ```langdetect``` library. The result export feature is used to export all the necessary features into a json file that are then store in the ```data/results/result.json```.

## Usage
If you wish to run the Text Analysis Tool through CLI, Just navigate to the ```main.py``` and run the python file. After that, it will ask you for which LLM model do you want to use. After that, it will ask you to put in a paragraph or essay for it to summarize. After that, you will have the summary and all the details about the paragraph you just put in.

Additionally, if you wish to run it through the web app, all you have to do is navigate to the folder and ```run streamlit run app.py``` and it will launch a web page in your browser. there will be a prompt bar on the screen where you can put in a paragraph or essay and it will summarize it, it will also provide you with the same type of choice where you can choose which LLM model you wish to use.
