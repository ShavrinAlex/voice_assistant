import webbrowser


class GoogleSearch:
    def __init__(self,voice):
        self.voice = voice

    def search(self):
        url = "https://www.google.com/search?q=" + self.voice.get_request()
        webbrowser.open(url)

  

