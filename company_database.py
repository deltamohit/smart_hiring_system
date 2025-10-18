# company_database.py

# Company → Job Roles → Required Skills mapping
# Skills are in preprocessed form (lowercase, stemmed)
COMPANY_JOB_SKILLS = {
    "Allianz Services": {
        "Associate-Customer Service": ["commun", "custom", "servic", "problem", "solv", "english", "crm", "support"]
    },
    "Amazon": {
        "Support Engineer III": ["linux", "troubleshoot", "network", "aws", "cloud", "support", "python", "sql"]
    },
    "Cognizant": {
        "Programmer Analyst Trainee": ["python", "java", "sql", "programm", "algorithm", "data", "structur", "oop"]
    },
    "Infosys": {
        "Specialist Programmer": ["java", "python", "spring", "microservic", "rest", "api", "sql"],
        "Systems Engineer Trainee": ["programm", "java", "python", "sql", "algorithm"],
        "Digital Specialist Engg": ["cloud", "devops", "docker", "kubernet", "python", "aws"]
    },
    "IBM": {
        "Software Developer": ["python", "java", "javascript", "sql", "cloud", "api", "develop"]
    },
    "UST": {
        "Developer I - Software Engineering.": ["python", "java", "javascript", "sql", "git", "web", "develop"],
        "Data Scientist": ["python", "machin", "learn", "statist", "sql", "data", "scienc", "model"]
    },
    "Equifax": {
        "Software Engineer": ["java", "python", "sql", "softwar", "develop", "api", "cloud"]
    },
    "Experion": {
        "Associate Software Engineer": ["python", "java", "javascript", "sql", "web", "develop", "git"]
    },
    "EY Gds": {
        "Associate Software Engineer": ["python", "java", "sql", "cloud", "develop", "algorithm"]
    },
    "Envestnet": {
        "Developer": ["java", "python", "sql", "develop", "api", "web"],
        "Engineer – QA": ["test", "qa", "selenium", "automat", "java", "python"],
        "Cloud Platform Engineer": ["cloud", "aws", "azure", "docker", "kubernet", "devops"]
    },
    "InApp": {
        "Associate Software Engineer": ["python", "java", "javascript", "react", "sql", "develop"]
    },
    "H&R Block": {
        "Associate Software Engineer": ["java", "python", "sql", "develop", "web", "api"]
    },
    "Mitsogo": {
        "Software Engineer": ["python", "java", "sql", "develop", "api"],
        "Product Evangelist": ["commun", "market", "product", "present", "technic"]
    },
    "NeoITO": {
        "Associate Software Engg": ["python", "javascript", "react", "sql", "web", "develop"],
        "Associate Ui/UX Designer": ["uiux", "figma", "design", "prototyp", "sketch"],
        "Associate Business Analyst": ["sql", "data", "analysi", "requir", "commun", "excel"]
    },
    "NexoMira": {
        "Software Engineer": ["python", "java", "javascript", "sql", "develop"]
    },
    "Simplogics": {
        "Software Engineer Trainee": ["python", "java", "sql", "develop", "programm"]
    },
    "ThinkPalm": {
        "Software Engineer Trainee": ["python", "java", "c", "embedd", "develop"]
    },
    "Cavli Wireless": {
        "Junior System Engineer": ["embedd", "c", "linux", "iot", "electr"]
    },
    "Honeywell": {
        "Embedded Engineer": ["embedd", "c", "microcontrol", "rtos", "electr"]
    },
    "Quest Global": {
        "Trainee Engineer": ["mechan", "design", "cad", "solidwork", "autocad"]
    },
    "CommandTech": {
        "Mechanical BIM Engineer": ["bim", "revit", "mechan", "design", "autocad"]
    },
    "Reflections Info Systems": {
        "Junior Data Engineer": ["python", "sql", "data", "etl", "spark", "hadoop"]
    },
    "Federal Bank": {
        "Customer Service Associate": ["commun", "custom", "servic", "financ", "bank", "english"]
    },
    "NSK": {
        "Graduate Trainee": ["mechan", "design", "manufactur", "qualiti", "process"]
    },
    "G10X": {
        "Internal Trainee": ["python", "java", "programm", "develop", "learn"]
    },
    # Add more companies as needed...
}

# Course recommendations (reusing from data_manager.py but you can customize)
SKILL_COURSE_MAP = {
    "python": "Python for Everybody - Coursera",
    "java": "Java Programming - Coursera",
    "sql": "SQL for Data Science - Coursera",
    "javascript": "JavaScript - The Complete Guide - Udemy",
    "react": "React - The Complete Guide - Udemy",
    "machin": "Machine Learning by Andrew Ng - Coursera",
    "cloud": "Cloud Computing Basics - Coursera",
    "aws": "AWS Certified Solutions Architect - Udemy",
    "docker": "Docker & Kubernetes - Udemy",
    "linux": "Linux Administration - Udemy",
    "embedd": "Embedded Systems - Coursera",
    "uiux": "UI/UX Design Specialization - Coursera",
    "data": "Data Science Specialization - Coursera",
    "commun": "Business Communication - Coursera",
    # Add more mappings as needed
}
