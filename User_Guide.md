# PETS-R-US Inventory System Documentation
# Purpose: An inventory system that is efficent and easy to use by employees and employers to track stock.

## Source File Documentation
Within each source file there are comments within the code that explain how certain aspects of the code works. Additionally, there are comments at the top of each file outling the developer(s), the purpose, and the usage of each file in relation to other files.

## User Guide
For an overview of the project respository, you will find several files and folders. At the top you will find a folder called backend that houses several files pertaining to the backend architecture of the database. There are database files, testing files, and an API file (also related to the database). The other two files that work in conjunction with the backend folder are the app.py file that houses Flask routes for web hosting, which will be discussed later on in this document, and the requirements.txt that describes what is needed to successfully run the Flask routes through web hosting on Render (a hosting website). The next folder is images and this houses various images from WEEKLY_UPDATES.md and a few demo web page designs from PAGE_TESTING.md. In the static folder, you will find three other folders: css, which houses the css design files for each web page, front_images, which houses the images and icons used on the web pages, and a javascript folder that holds the javascript that adds functionality for each web page. In the last folder, titled templates, it houses the HTML pages that the web pages are based upon.

### How to run/ view project
**On Render (web hosting service): ** This is the preferred method of use until the web service expires, which after that it will have to be run locally. Go to the README.md in the project repository and click on the Render Link towards the bottom of the document. This will take you to the web service where you can play around with the project. If the service is too slow or not working, please find a demo of the project via the link on the README.md file.

**On a local machine:** make sure to have all the files downloaded, especially the app.py file, and go to the repository folder on your machine through the command line. Type in "flask run" to a new command line, and click on the link to display on a local port in your browser of choice. Please note, database connection issues may be more pronounced when running on a local machine.

### Features:
- Clickable web links and buttons that go between web pages
- Database integration of user login information, product inventory, supplier information, and more for ease of finding information about the inventory quickly

### Known bugs:
- The database does not fully connect automatically through the web hosting service, and many times products and table information ahve to be added manually using the external database link and SQL code on a local machine.
- Displaying the username when someone logs in on the search page doesn't work as intended as the database is not connecting properly.
- The login and create account forms are not very secure as time was limited to complete the project and a lack of knowledge of some security principles posed challenges to getting it to be secure by the project deadline.

## Project Documentation
Within the project there are files that outline Milestone achievements for different aspects of the project throughout the semester. These files outline different plans and achievements of the project and the developers' tasks throughout the timeline project. The files include WEEKLY_UPDATES.md, SQL_TESTING.md, PAGE_TESTING.md, README.md, FINAL_REPORT.md, PETS-R-US_Presentation.pdf, and the UI mockup PETS-R-US_Inventory_System.pdf.
