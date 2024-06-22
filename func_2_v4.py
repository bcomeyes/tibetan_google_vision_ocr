from google.cloud import vision_v1
from google.cloud import storage

#This function will read your images stored in cloud storage automatically
def list_objects(bucket,prefix):
    obj_arr = []
    client = storage.Client()
    for blob in client.list_blobs(bucket, prefix=prefix):
        obj_arr.append(f"gs://{gcs}/{blob.name}")
    print(obj_arr[1:])
    return obj_arr[1:]


def sample_batch_annotate_images(uri_arr,output_uri):
    """Perform async batch image annotation."""
    client = vision_v1.ImageAnnotatorClient()

    #You can add/remove here the feature types you want
    features = [
            {"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}
        ]

    requests = []

    #this will append the images you have stored in array_of_gcs_uri from Cloud Storage
    for uri in uri_arr:
        source = {"image_uri": uri} #url1
        image = {"source": source}
        image_context = {"language_hints": ["bo-t-bo"]}
        request = {"image": image, "features": features, "image_context": image_context}
        requests.append(request)

    print(requests)

    response = client.batch_annotate_images(requests=requests)
        
    for response in response.responses:
        with open("tibetan_v3.txt","a",encoding="utf-8") as o:
            o.write('"{}"'.format(response.full_text_annotation.text))
        print(response.full_text_annotation.text)
    
  
gcs="image-bucket-ocr-3-23-2022" #ex. gcs="vision_test"
folder="multi_file_image_directory" #ex. gcs="all_images"
array_of_gcs_uri = list_objects(bucket=gcs,prefix=folder)

destination_uri = "gs://destination_bucket/" 

sample_batch_annotate_images(uri_arr=array_of_gcs_uri,output_uri=destination_uri)
