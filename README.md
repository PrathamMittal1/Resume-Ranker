# Resume-Ranker
## Resume parsing and ranking of resumes in accordance to a given job description.

Resume shortlisting is a very tedious task in a hiring process, especially when the number of candidates is high. Each candidate is good at something and comparison of them is a very tuff job.
Resume Ranker is a project with the motive of easing the resume shortlisting job by selecting the top most resumes from a huge pile of resumes.
It can select resumes on basis of job description or comparing all the resumes with each other. In the latter one, the resume with most score survives.

It is a graphical user interface (GUI) application using the Tkinter library for a Resume Ranker system. Here are some highlights of the work undertaken in this project:

•	User Interface: The application has a graphical user interface built with Tkinter, providing a visually appealing and user-friendly environment for users to interact with the system.

•	File Handling: The program includes functionality for users to select multiple CV (resume) files using a file dialog. It then processes and extracts data from these files for further analysis.

•	Job Description Processing: The system allows users to input or edit a job description, which is a crucial element in matching candidates to job requirements. The entered job description is saved and used for processing resumes.

•	Resume Processing: Resumes are processed using a CV_processing module, which likely contains functions to read and extract relevant information from resume files. The extracted data is then used for further analysis.
•	Data Analysis and Sorting: The program utilizes the Pandas library to create a DataFrame for storing and analyzing the extracted data from resumes. The data is sorted based on a "Match Score" in descending order, indicating how well each candidate matches the given job description.

•	Tabulation and Display: The tabulate library is used to format the DataFrame for display purposes. The ranked data is presented in a tabular format within the Tkinter GUI, allowing users to easily view and interpret the results.

•	Maximized View: The system provides a button for users to view the tabulated data in an enlarged, full-screen window. This enhances the user experience by allowing a more detailed examination of the ranked resumes.

•	Save Job Description: Users have the ability to edit the job description and save the changes for future use. The edited job description is stored in a text file (Data/Job Description.txt).

•	Enhanced User Interaction: The application includes buttons for users to navigate between different pages of the system, such as selecting resumes, processing data, and viewing the results.

•	Scrolled Text Widget: The use of the scrolled text widget (scrolledtext) provides a convenient way to display large amounts of text, such as the list of selected resume files and the tabulated results.


Overall, the project demonstrates proficiency in GUI development, file handling, data processing, and the integration of various Python libraries for a practical application in the context of resume ranking.

