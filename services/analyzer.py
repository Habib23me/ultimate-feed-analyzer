import io
import os
from google.cloud import vision
from google.cloud import language_v1
from data_model.activity import Activity
from data_model.feature_response import FeatureResponse
from dotenv import load_dotenv
load_dotenv()


imageclient = vision.ImageAnnotatorClient()
langagueClient = language_v1.LanguageServiceClient()


def analyseLocalMedia(foreign_id, medias):
    analysed_data = []

    # The name of the image file to annotate
    for media in medias:
        file_name = os.path.abspath(media)
        # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    # Performs label detection on the image file
    response = imageclient.label_detection(image=image)
    labels = response.label_annotations
    for label in labels:
        data = FeatureResponse(foreign_id, label.description, label.score)
        analysed_data.append(data)
    return analysed_data


def analyseRemoteMedia(foreign_id, medias):
    analysed_data = []

    # The name of the image file to annotate
    for media in medias:
        image = vision.Image()
        image.source.image_uri = os.environ['PREFIX_MEDIA_URL']+media
        response = imageclient.label_detection(image=image)
        labels = response.label_annotations
        for label in labels:
            if(label.score > 0.5):
                data = FeatureResponse(
                    foreign_id, label.description, label.score)
                analysed_data.append(data)
    return analysed_data


def analyseCaption(foreign_id, caption):
    if caption is None:
        return []
    analysed_data = []

    # The text to analyze
    document = language_v1.Document(
        content=caption, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    # Detects the sentiment of the text
    entities = langagueClient.analyze_entities(
        request={"document": document}
    ).entities

    for entity in entities:
        if(entity.salience > 0.5):
            data = FeatureResponse(foreign_id, entity.name, entity.salience)
            analysed_data.append(data)

    return analysed_data


def analyseActivity(activity: Activity):
    textLabels = analyseCaption(activity.foreign_id, activity.caption)
    imageLabels = analyseRemoteMedia(activity.foreign_id, activity.media)

    # write a row to the csv file
    datas = textLabels+imageLabels

    # sort data by score and pick top 5
    datas.sort(key=lambda x: x.score, reverse=True)
    datas = datas[:5]
    return datas
