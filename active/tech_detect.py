import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from Wappalyzer import Wappalyzer, WebPage

def detect_tech(domain):
    try:
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url(f"http://{domain}")
        return wappalyzer.analyze(webpage)
    except Exception as e:
        return {"error": str(e)}
