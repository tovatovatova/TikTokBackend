

def get_results_template():
    return {
        "score": -1,
        "details": {
            "video_results": { "score": 7, "details": [{ "image_url": "http://localhost:5000/images/frame_30", "reason": "This Frame Has too much red and does not stand with the policy" }] },
            "audio_results": { "score": -1, "details": [{ "word": "killing", "reason": "Killing is Bad" }] },
            "text_results": { "score": 9, "details": [{ "word": "killing", "reason": "Killing is Bad", "image_url": "http://localhost:5000/images/frame_30" }] },
            "static_results": { "score": 8, "details": { "width": 1280, "height": 720, "bitrate": 128_000, "snr": 8 }},
        }
    }
    
def calc_final_score(results):
    all_results = results['details'].values()
    return sum(float(v['score']) for v in all_results) / len(all_results)