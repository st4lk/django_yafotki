# coding: utf-8

try:
    from redactor.handlers import BaseUploaderRedactor
    from .storage import YFStorage

    class FotkiUploader(BaseUploaderRedactor):
        def save_file(self):
            self.url = YFStorage().save('image', self.upload_file)

        def get_filename(self):
            return u""

        def get_url(self):
            return self.url

except ImportError:
    pass

