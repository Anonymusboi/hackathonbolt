# backend/matching.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import JobListing, JobSeeker

class JobMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def match_jobs_to_seeker(self, job_seeker, jobs):
        # Combine skills and experience for the seeker
        seeker_text = f"{job_seeker.skills} {job_seeker.experience}"
        
        # Prepare job descriptions
        job_texts = [f"{job.title} {job.description} {job.skills_required}" for job in jobs]
        all_texts = [seeker_text] + job_texts
        
        # Vectorize text
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        # Calculate similarity
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        # Get top matches (limit to 10)
        similar_indices = cosine_similarities.argsort()[0][-10:][::-1]
        matched_jobs = [(jobs[i], cosine_similarities[0][i]) for i in similar_indices]
        
        return matched_jobs
    
    def match_seekers_to_job(self, job, seekers):
        # Combine job details
        job_text = f"{job.title} {job.description} {job.skills_required}"
        
        # Prepare seeker profiles
        seeker_texts = [f"{seeker.skills} {seeker.experience}" for seeker in seekers]
        all_texts = [job_text] + seeker_texts
        
        # Vectorize text
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        
        # Calculate similarity
        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        # Get top matches (limit to 10)
        similar_indices = cosine_similarities.argsort()[0][-10:][::-1]
        matched_seekers = [(seekers[i], cosine_similarities[0][i]) for i in similar_indices]
        
        return matched_seekers