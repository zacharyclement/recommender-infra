from typing import Dict, List

from fastapi import FastAPI, HTTPException

# Initialize the FastAPI app
app = FastAPI()


# Original get_trending_livestreams function
def get_trending_livestreams() -> List[Dict]:
    """
    Gets a list of trending livestreams.

    Returns:
        sorted_livestreams (List[dict]): A list of dictionaries containing livestream IDs and a trendiness score.
    """
    # Example placeholders for required methods
    active_livestream_ids = get_active_livestream_ids()
    model = get_model()
    scores = model.predict(active_livestream_ids)

    livestreams_w_scores = []
    for livestream_id in active_livestream_ids:
        score = scores.get(livestream_id, default=None)
        if score:
            livestreams_w_scores.append(
                {
                    "livestream_id": livestream_id,
                    "score": score,
                }
            )

    sorted_livestreams = sorted(
        livestreams_w_scores,
        key=lambda x: x["score"],
        reverse=True,
    )
    return sorted_livestreams


# Mock implementations of required methods
def get_active_livestream_ids():
    return [1, 2, 3, 4]


def get_model():
    class MockModel:
        def predict(self, ids):
            return {id_: 1.0 / (id_ + 1) for id_ in ids}

    return MockModel()


# FastAPI endpoint for get_trending_livestreams
@app.get("/get_trending_livestreams")
def api_get_trending_livestreams():
    try:
        trending_livestreams = get_trending_livestreams()
        return trending_livestreams
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
