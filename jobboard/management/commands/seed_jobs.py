from django.core.management.base import BaseCommand
from jobboard.models import CustomUser, Job

class Command(BaseCommand):
    help = 'Seed jobs into database'

    def handle(self, *args, **kwargs):
        # Create employer if not exists
        employer, created = CustomUser.objects.get_or_create(
            username='techcorp_hr',
            defaults={
                'email': 'hr@techcorp.com',
                'role': 'employer',
                'company_name': 'TechCorp',
            }
        )
        if created:
            employer.set_password('Admin@1234')
            employer.save()

        jobs = [
            {"title": "React Developer", "company": "TechCorp", "location": "Bangalore", "job_type": "full_time", "description": "Build modern web applications using React.js and REST APIs.", "requirements": "React.js, JavaScript, CSS, REST APIs, Git. Min 1 year experience.", "salary": "5-8 LPA"},
            {"title": "Backend Developer", "company": "Infosys", "location": "Hyderabad", "job_type": "full_time", "description": "Develop scalable backend services using Django and PostgreSQL.", "requirements": "Django, Python, PostgreSQL, REST APIs. Min 1 year experience.", "salary": "6-10 LPA"},
            {"title": "Frontend Developer", "company": "Wipro", "location": "Chennai", "job_type": "full_time", "description": "Create responsive UI components using React and TailwindCSS.", "requirements": "React.js, HTML, CSS, JavaScript, TailwindCSS.", "salary": "4-7 LPA"},
            {"title": "Full Stack Developer", "company": "TCS", "location": "Mumbai", "job_type": "full_time", "description": "Work on end-to-end features from database to frontend.", "requirements": "React.js, Node.js or Django, PostgreSQL, Git.", "salary": "7-12 LPA"},
            {"title": "Python Developer", "company": "HCL Technologies", "location": "Pune", "job_type": "full_time", "description": "Write clean Python code for automation and backend services.", "requirements": "Python, Django, REST APIs, MySQL.", "salary": "5-9 LPA"},
            {"title": "Django Developer", "company": "Zoho", "location": "Chennai", "job_type": "full_time", "description": "Build and maintain Django REST APIs for enterprise applications.", "requirements": "Django, DRF, PostgreSQL, JWT Auth.", "salary": "6-10 LPA"},
            {"title": "Data Analyst", "company": "Accenture", "location": "Bangalore", "job_type": "full_time", "description": "Analyze large datasets and build reports using Python and Power BI.", "requirements": "Python, Pandas, SQL, Power BI, Excel.", "salary": "5-8 LPA"},
            {"title": "DevOps Engineer", "company": "Amazon", "location": "Hyderabad", "job_type": "full_time", "description": "Manage CI/CD pipelines, Docker containers and AWS infrastructure.", "requirements": "Docker, Kubernetes, AWS, Jenkins, Linux.", "salary": "10-18 LPA"},
            {"title": "Android Developer", "company": "Flipkart", "location": "Bangalore", "job_type": "full_time", "description": "Build and maintain Android apps for millions of users.", "requirements": "Java, Kotlin, Android SDK, REST APIs.", "salary": "8-14 LPA"},
            {"title": "UI/UX Designer", "company": "Swiggy", "location": "Bangalore", "job_type": "full_time", "description": "Design intuitive user interfaces and improve user experience.", "requirements": "Figma, Adobe XD, Wireframing, Prototyping.", "salary": "6-10 LPA"},
            {"title": "Machine Learning Engineer", "company": "Google", "location": "Hyderabad", "job_type": "full_time", "description": "Build and deploy machine learning models at scale.", "requirements": "Python, TensorFlow, PyTorch, Scikit-learn, SQL.", "salary": "20-35 LPA"},
            {"title": "Java Developer", "company": "Oracle", "location": "Bangalore", "job_type": "full_time", "description": "Develop enterprise Java applications using Spring Boot.", "requirements": "Java, Spring Boot, Hibernate, MySQL, Maven.", "salary": "7-12 LPA"},
            {"title": "Web Developer Intern", "company": "StartupXYZ", "location": "Remote", "job_type": "internship", "description": "Work on real projects and learn modern web development.", "requirements": "HTML, CSS, JavaScript, basic React knowledge.", "salary": "10,000-15,000/month"},
            {"title": "Software Developer", "company": "Microsoft", "location": "Hyderabad", "job_type": "full_time", "description": "Build scalable software solutions for Microsoft products.", "requirements": "C++, Python or Java, Data Structures, Algorithms.", "salary": "25-40 LPA"},
            {"title": "Node.js Developer", "company": "PayPal", "location": "Chennai", "job_type": "full_time", "description": "Build high-performance APIs using Node.js and Express.", "requirements": "Node.js, Express, MongoDB, REST APIs, JWT.", "salary": "8-14 LPA"},
            {"title": "React Native Developer", "company": "PhonePe", "location": "Bangalore", "job_type": "full_time", "description": "Build cross-platform mobile apps using React Native.", "requirements": "React Native, JavaScript, Redux, REST APIs.", "salary": "9-15 LPA"},
            {"title": "Cloud Engineer", "company": "IBM", "location": "Pune", "job_type": "full_time", "description": "Design and manage cloud infrastructure on AWS and Azure.", "requirements": "AWS, Azure, Terraform, Docker, Linux.", "salary": "10-18 LPA"},
            {"title": "QA Engineer", "company": "Cognizant", "location": "Mumbai", "job_type": "full_time", "description": "Write automated test cases and ensure software quality.", "requirements": "Selenium, Python, Pytest, JIRA, Agile.", "salary": "4-7 LPA"},
            {"title": "Data Engineer", "company": "Uber", "location": "Hyderabad", "job_type": "full_time", "description": "Build data pipelines and manage large scale data processing.", "requirements": "Python, Apache Spark, Hadoop, SQL, Airflow.", "salary": "12-20 LPA"},
            {"title": "Cybersecurity Analyst", "company": "Deloitte", "location": "Gurgaon", "job_type": "full_time", "description": "Monitor and protect systems from security threats.", "requirements": "Network Security, Ethical Hacking, SIEM, Python.", "salary": "8-15 LPA"},
            {"title": "Flutter Developer", "company": "Ola", "location": "Bangalore", "job_type": "full_time", "description": "Build beautiful cross platform apps using Flutter and Dart.", "requirements": "Flutter, Dart, REST APIs, Firebase.", "salary": "7-12 LPA"},
            {"title": "Blockchain Developer", "company": "CoinDCX", "location": "Mumbai", "job_type": "full_time", "description": "Build smart contracts and decentralized applications.", "requirements": "Solidity, Ethereum, Web3.js, JavaScript.", "salary": "12-22 LPA"},
            {"title": "iOS Developer", "company": "Meesho", "location": "Bangalore", "job_type": "full_time", "description": "Build and maintain iOS applications using Swift.", "requirements": "Swift, Xcode, UIKit, REST APIs, Git.", "salary": "10-18 LPA"},
            {"title": "Part Time Web Developer", "company": "FreelanceHub", "location": "Remote", "job_type": "part_time", "description": "Work part time on web projects from home.", "requirements": "HTML, CSS, JavaScript, WordPress.", "salary": "20,000-30,000/month"},
            {"title": "Angular Developer", "company": "Capgemini", "location": "Noida", "job_type": "full_time", "description": "Build enterprise web apps using Angular and TypeScript.", "requirements": "Angular, TypeScript, RxJS, REST APIs.", "salary": "6-10 LPA"},
            {"title": "Database Administrator", "company": "Tech Mahindra", "location": "Pune", "job_type": "full_time", "description": "Manage and optimize PostgreSQL and MySQL databases.", "requirements": "PostgreSQL, MySQL, Query Optimization, Backup & Recovery.", "salary": "6-10 LPA"},
            {"title": "Embedded Systems Engineer", "company": "Bosch", "location": "Bangalore", "job_type": "full_time", "description": "Develop firmware for embedded hardware systems.", "requirements": "C, C++, RTOS, ARM architecture, UART/SPI/I2C.", "salary": "7-12 LPA"},
            {"title": "Product Manager", "company": "Razorpay", "location": "Bangalore", "job_type": "full_time", "description": "Define product roadmap and work with engineering teams.", "requirements": "Product thinking, Agile, Jira, SQL, Communication skills.", "salary": "15-25 LPA"},
            {"title": "Scrum Master", "company": "Mindtree", "location": "Hyderabad", "job_type": "full_time", "description": "Facilitate agile ceremonies and remove blockers for teams.", "requirements": "Scrum, Kanban, Jira, Agile coaching. CSM certification preferred.", "salary": "8-14 LPA"},
            {"title": "Technical Support Engineer", "company": "Dell", "location": "Chennai", "job_type": "full_time", "description": "Provide technical support and troubleshooting for Dell products.", "requirements": "Technical knowledge of Dell products, Communication skills, Problem-solving.", "salary": "4-7 LPA"},
            {"title": "Business Analyst", "company": "Mphasis", "location": "Chennai", "job_type": "full_time", "description": "Bridge gap between business and technical teams.", "requirements": "Requirement gathering, SQL, JIRA, Agile, Communication.", "salary": "6-10 LPA"},
        ]

        for job_data in jobs:
            Job.objects.get_or_create(
                title=job_data['title'],
                company=job_data['company'],
                defaults={**job_data, 'employer': employer}
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(jobs)} jobs!'))