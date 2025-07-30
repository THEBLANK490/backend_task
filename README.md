# Backend Task Project

## Setup
1. Clone repository: `git clone https://github.com/THEBLANK490/backend_task.git`
2. Create `.env` file with environment variables
3. Build containers: `docker-compose up -d --build`
4. Apply migrations: `docker-compose exec django python manage.py migrate`
5. Create superuser: `docker-compose exec django python manage.py createsuperuser`

## API Usage
1. Get user vector line:  
   `GET /api/line/<user_id>/geojson/`
   
2. Find nearby users:  
   `GET /api/nearby/?lat=27.7172&lng=85.3240`

3. Visualize data in elasticsearch:
    `go to the http://localhost:5601/app/home#/ to access kibana`
 

## Scheduled Tasks
- Hydrology data ingestion runs every 5 minutes via Celery Beat

## Assumptions & Enhancements
- Used PostGIS for geographical operations
- Added distance calculation in user model
- Implemented retry mechanism for data ingestion
- Used GeoJSON for vector line response
- Added custom manager for spatial queries
- Optimized Elasticsearch indexing with bulk operations