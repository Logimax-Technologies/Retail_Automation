import time,re
import base64
import warnings
import requests
import pdfplumber
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib3.exceptions import InsecureRequestWarning



# silence insecure request warning (dev/test only)
warnings.simplefilter('ignore', InsecureRequestWarning)


class EstimationExtractor:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    def _download_with_cookies_ignore_ssl(self, url: str, out_path: str):
        sess = requests.Session()
        for c in self.driver.get_cookies():
            # set cookie simple name/value
            sess.cookies.set(c['name'], c.get('value', ''))
        # IMPORTANT: verify=False disables SSL cert validation (dev only)
        r = sess.get(url, stream=True, timeout=30, verify=False)
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
        return out_path

    def _save_blob_via_browser(self, blob_url: str, out_path: str):
        # Browser fetch to get bytes and return base64 -> write file
        script = """
        const url = arguments[0];
        const callback = arguments[arguments.length-1];
        fetch(url).then(r => r.arrayBuffer())
          .then(buf => {
            let binary = '';
            let bytes = new Uint8Array(buf);
            const chunk = 0x8000;
            for (let i=0; i<bytes.length; i+=chunk) {
              binary += String.fromCharCode.apply(null, bytes.subarray(i, i+chunk));
            }
            callback(btoa(binary));
          })
          .catch(err => callback(null));
        """
        b64 = self.driver.execute_async_script(script, blob_url)
        if not b64:
            raise RuntimeError("Browser fetch of blob failed.")
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(b64))
        return out_path

    def save_and_extract(self, out_pdf="customer_copy.pdf", viewer_url: str = None):
        """
        If viewer_url provided, uses it; otherwise reads current tab's URL.
        Returns tuple (out_pdf_path, full_text).
        """
        # If viewer_url not given, use current URL
        url = viewer_url or self.driver.current_url
        # Make absolute if relative
        if viewer_url and not viewer_url.lower().startswith(("http://", "https://", "blob:", "data:")):
            url = urljoin(self.driver.current_url, viewer_url)

        print("Detected PDF source:", url)

        # handle data: (base64) or blob or http(s)
        if url.startswith("data:"):
            # data:[<mediatype>][;base64],<data>
            header, b64 = url.split(',', 1)
            with open(out_pdf, "wb") as f:
                f.write(base64.b64decode(b64))
            saved = out_pdf
        elif url.startswith("blob:"):
            # fetch via browser
            saved = self._save_blob_via_browser(url, out_pdf)
        else:
            # http/https - try browser fetch first to avoid python SSL issues, fallback to requests verify=False
            try:
                # attempt browser fetch (works if same-origin / accessible)
                saved = self._save_blob_via_browser(url, out_pdf)
            except Exception:
                # fallback to requests (with cookies) ignoring SSL verification (dev)
                saved = self._download_with_cookies_ignore_ssl(url, out_pdf)

        # Extract all text with pdfplumber
        with pdfplumber.open(saved) as pdf:
                data = {
                    "Estimate": None,
                    "cgst": "0.00",
                    "sgst": "0.00",
                    "igst": "0.00",
                    "total": "0.00"
                }
                page=pdf.pages[0]
                text = page.extract_text()
                for line in text.split('\n'):
                    # print(line)
                    estimate=re.search(r"Estimate\s*[:\-]?\s*(\d+)", line, re.I) 
                    if estimate:
                        data["Estimate"] = estimate.group(1)
                        print("Estimate =", data["Estimate"])
                        
                    cgst=re.search(r"CGST.*?\s+([\d,]+\.\d{2})\s*$", line, re.I)
                    if cgst:
                        data["cgst"] = cgst.group(1)
                        print("Cgst =", data["cgst"])

                    sgst=re.search(r"SGST.*?\s+([\d,]+\.\d{2})\s*$", line, re.I)
                    if sgst:
                        data["sgst"] = sgst.group(1)
                        print("Sgst =", data["sgst"])

                    igst=re.search(r"IGST.*?\s+([\d,]+\.\d{2})\s*$", line, re.I)
                    if igst:
                        data["igst"] = igst.group(1)
                        print("Igst =", data["igst"])

                    # Corrected Total extraction: Check second pattern only if first fails to avoid double entries
                    total=re.search(r"^Total\s*:\s*Rs\.?\s*([\d,]+\.\d{2})", line, re.I)
                    if total:
                        data["total"] = total.group(1)
                        print("Total =", data["total"])
                    else:
                        total=re.search(r"^Total\s*:\s*Rs\.?\s*(-?[\d,]+\.\d{2})", line, re.I)
                        if total:
                            data["total"] = total.group(1)
                            print("Total =", data["total"])
                
                print(data)    
                return data
