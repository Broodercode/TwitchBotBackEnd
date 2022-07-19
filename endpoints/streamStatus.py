from helpers.db_helpers import run_query
from flask import request
from app import app


@app.post('/stream-updates')
def stream_update():
    print('stream update reached')
    data = request.json
    print(data)

    for i in data:
        if i != 'update':
            raw_started_at = i.get('started_at')
            started_at = raw_started_at.replace('T', ' ').replace('Z', '')
            stream_id = i.get('stream_id')
            room_id = i.get('user_id')
            viewer_count = i.get('viewer_count')
            streamer_name = i.get('user_login')
            log_time = i.get('log_time')
            post_data = [started_at, stream_id,
                         room_id, viewer_count, streamer_name, log_time]
            stream_data = [started_at, stream_id, room_id, streamer_name]
            viewer_data= [log_time, viewer_count, stream_id]
            print(i)
            print(post_data)
            run_query(
                'INSERT INTO streams (started_at, stream_id, room_id, streamer_name) VALUES (?,?,?,?)', stream_data
            )
            print('viewer_log query')
            run_query(
                'INSERT INTO viewer_logs (logtime, viewer_count, stream_id) VALUES (?,?,?)', viewer_data)

    return 'update success'


@app.patch('/stream-updates')
def stream_patch():
    print('stream end reached')
    data = request.json
    print(data)

    stream_id = data['stream_id']
    print(stream_id)
    ended_at = data['ended_at']
    print(ended_at)
    run_query('UPDATE streams SET ended_at = ? WHERE stream_id=?',
            [ended_at, stream_id])
    return 'end success'
