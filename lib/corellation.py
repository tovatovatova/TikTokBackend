

def get_results_template():
    return {
        "score": 6,
        "details": {
            "video_results": { "score": 4, "details": [{ "image_url": "http://localhost:5000/images/frame_30.jpg", "reason": "The image shows individuals in military gear with firearms, by a pickup truck at night, potentially violating platforms' guidelines against violence." }] },
            "audio_results": { "score": 10, "details": [] },
            "text_results": { "score": 5, "details": [{ "word": "knife, hostage", "reason": "The words 'knife' and 'hostage' might violate community guidelines because they are associated with violence, threats, and danger to life", "image_url": "http://localhost:5000/images/frame_20.jpg" }] },
            "static_results": { "score": 8, "details": { "width": 1280, "height": 720, "bitrate": 8_000_000, "snr": 8 }},
        }
    }


def calc_final_score(results):
    all_results = results['details'].values()
    return sum(float(v['score']) for v in all_results) / len(all_results)
