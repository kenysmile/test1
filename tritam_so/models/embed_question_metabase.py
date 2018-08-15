# -*- coding: utf-8 -*-
import jwt

def embed_question_metabase(ID,METABASE_SITE_URL,METABASE_SECRET_KEY,param):
    payload = {
        "resource": {"question": int(ID)},
        "params": param,
    }
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    return (METABASE_SITE_URL + "/embed/question/" + token.decode("utf8") + "#bordered=true&titled=true")