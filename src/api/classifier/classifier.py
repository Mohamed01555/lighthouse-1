"""
Original file is located at
    https://colab.research.google.com/drive/1EltssuA0Fa_uX_ZRBbf51EtxqPmTt6XT
"""

import insightface
from PIL import Image
from numpy import asarray, dot


class ImageClassifier:
    def __init__(self):
        self.model = insightface.app.FaceAnalysis(
            det_name="retinaface_mnet025_v2", rec_name="arcface_r100_v1", ga_name=None
        )
        self.model.prepare(ctx_id=-1, nms=0.4)
        # ctx_id = -1 to use CPU

    @staticmethod
    def prepare_image(filename):
        image = Image.open(filename).convert("RGB")
        pixels = asarray(image)
        return pixels

    def get_face_info(self, pixels):
        """This function takes an image and extracts
        laocation of faces in the image and normed embedding of them.
        InsightFace performs both extraction and embedding.
        """
        return self.model.get(pixels)

    def embed(self, image):
        """Returns the embedding of face or faces in the image."""

        pixels = self.prepare_image(image)
        results = self.get_face_info(pixels)
        # TODO: fixing problem of multiple faces in the same photo
        return results[0].normed_embedding

    def get_similarity(self, face1, face2):
        face1_emb = self.embed(face1)
        face2_emb = self.embed(face2)
        cos_sim = dot(face1_emb, asarray(face2_emb).T)
        return cos_sim

    # TODO: make imagesEmbeds dynamic
    def find(self, image, image_list):
        most_similar = {"pk": -1, "value": -1}
        for pk, source_image in image_list.items():
            similarity = self.get_similarity(source_image, image)
            if similarity > most_similar["value"]:
                most_similar["index"] = pk
                most_similar["value"] = similarity
        return most_similar


class ImageClassifierSimulator:
    @staticmethod
    def find(image, image_list):
        most_similar = {"pk": -1, "value": -1}
        return most_similar
