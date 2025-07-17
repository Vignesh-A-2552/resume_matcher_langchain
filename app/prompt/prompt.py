match_template ="""
Compare the following resume and job description and give a match score (0-100%) with a 1-line justification.

Resume: {resume}
Job Description: {jd}

Output:
Match Score:
Reason:
"""

question_template = """
Generate 5 specific interview questions for the candidate whose resume is below, tailored to the job description.

Resume:
{resume}

Job Description:
{jd}

Questions:
"""