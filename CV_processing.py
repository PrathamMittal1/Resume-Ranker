import docx2txt
import re
from pdfminer.high_level import extract_text
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def readResume(path, jd):
    if path[-3:].lower() == 'pdf':
        text = extract_text(path)
    else:
        text = docx2txt.process(path)

    data = dict()

    data['Name'] = text.strip().split('\n')[0]
    # -------------------------------------------------------------------
    data['Contact number'] = None
    mat = re.search(r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
                    text, re.IGNORECASE)  # phone number matching
    if mat:
        data['Contact number'] = mat.group()
    # --------------------------------------------------------------------
    data['Email'] = None
    mat = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                    text, re.IGNORECASE)  # email matching
    if mat:
        data['Email'] = mat.group()
    # --------------------------------------------------------------------
    data['College'] = None  # Extracting college name
    pattern = re.compile(r".*?\b(?:college|university|institute|school)\s+(?:of\s+)?[\w\s-]+.*",
                         re.IGNORECASE)
    data['College'] = ', '.join(pattern.findall(text))
    # ---------------------------------------------------------------------
    data['Degree'] = None  # Degree extraction
    pattern = re.compile(r".*\b(?:bachelor|bachelors|master|masters|b.tech|m.tech)\b.*",
                         re.IGNORECASE)
    data['Degree'] = ', '.join(pattern.findall(text))
    # ---------------------------------------------------------------------
    skills_list = ['Cloud', 'Python', 'Machine Learning', 'Artificial Intelligence', 'Java', 'Flutter', 'Programming',
                   'Theory and Mathematics of Computation', 'Problem Analysis', 'Programming Languages', 'Data Science',
                   'Computing', 'Web development', 'React', 'Nodejs', 'Coding', 'Golang', 'Cyber', 'Angular',
                   'Big Data', 'Deep Learning', 'Natural Language Processing', 'Computer Vision',
                   'Software Development',
                   'Frontend Development', 'Backend development', 'Algorithms', 'Software Engineering', 'Data analysis',
                   'Database Management', 'Cloud Computing', 'IoT', 'BlockChain', 'Mobile App Development', 'DevOps',
                   'Network Security', 'CyberSecurity', 'Cloud Architecture', 'Robotics', 'Game Development',
                   'agile methodology', 'version Control', 'Virtual Reality', 'Augmented Reality', 'Data Mining',
                   'Ethics in AI', 'Quantum Computing', 'Hadoop', 'Spark', 'Mongodb', 'NOSQL Databases', 'UI/UX Design',
                   'Responsive Web Design', 'API Development', 'IoT Devices', 'Cryptography', 'Automation',
                   'System Administration', 'Web Frameworks', 'Docker', 'Kubernetes', 'Microservices', 'Cloud Services',
                   'Serverless Architecture', 'API', 'Shell', 'Linux', 'Windows',
                   'AR/VR', 'Data Visualization', 'Business Intelligence', 'Data Engineering',
                   'Optimization',
                   'Parallel Computing', 'Game Engines', 'Distributed Systems', 'Network Protocols',
                   'Scalability', 'Edge Computing', 'Quantum', 'Quantum Programming', 'Bioinformatics',
                   'Robotics', 'Computer-Aided Design', 'CAD', 'Cloud Security', 'Ethical Hacking',
                   'Penetration Testing', 'Digital Forensics', 'Machine Translation',
                   'E-commerce', 'Ethics', 'Embedded Systems', 'FPGA', 'Wireless Communication',
                   'Sensor', 'AI', 'Natural Language Processing', 'NLP']
    data['Skills'] = None
    skills = []
    for skill in skills_list:  # skills matching
        pattern = r"\b{}\b".format(re.escape(skill))
        mat = re.search(pattern, text, re.IGNORECASE)
        if mat:
            skills.append(skill)
    data['Skills'] = ','.join(skills)
    # -----------------------------------------------------------------
    for key, val in data.items():
        t = ''
        if type(val) == type(list):
            t = ', '.join(val)
            data[key] = t

    cv = CountVectorizer()  # Using cosine similarity to find similarities in jd and resume
    matrix = cv.fit_transform((text, jd))
    similarity_matrix = cosine_similarity(matrix)
    # print(similarity_matrix)
    data['Match Score'] = round(similarity_matrix[0][1] * 100, 2)
    return data
