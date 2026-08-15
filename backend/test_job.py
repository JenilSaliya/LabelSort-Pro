from app.services.job.job_service import JobService

service = JobService()

job = service.create_job()

print(job)