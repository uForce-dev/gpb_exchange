import logging
import uuid
import xml.etree.ElementTree as ET
from typing import Any

from lxml import etree
from pathlib import Path

from flask import Flask, request, Response

BASE_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(BASE_DIR / "logs/app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def validate_xml(xml_string: str | Path, xsd_path: str | Path) -> [bool, tuple[Any, Any]]:
    with open(xsd_path, "rb") as xsd_file:
        schema_root = etree.XML(xsd_file.read())
        schema = etree.XMLSchema(schema_root)

    xml_doc = etree.fromstring(xml_string)
    return schema.validate(xml_doc), schema.error_log


def create_cpa_res(
    result_code, result_desc=None, merchant_trx=None, purchase_data=None
):
    root = ET.Element("payment-avail-response")

    result = ET.SubElement(root, "result")
    code = ET.SubElement(result, "code")
    code.text = str(result_code)

    if result_desc:
        desc = ET.SubElement(result, "desc")
        desc.text = result_desc

    if merchant_trx:
        merchant_trx_elem = ET.SubElement(root, "merchant-trx")
        merchant_trx_elem.text = merchant_trx

    if result_code == 1 and purchase_data:
        purchase = ET.SubElement(root, "purchase")

        short_desc_text = purchase_data.get("shortDesc", "")
        if short_desc_text:
            short_desc = ET.SubElement(purchase, "shortDesc")
            short_desc.text = purchase_data.get("shortDesc", "")

        long_desc = ET.SubElement(purchase, "longDesc")
        long_desc.text = purchase_data.get("longDesc", "")

        account_amount = ET.SubElement(purchase, "account-amount")
        id_elem = ET.SubElement(account_amount, "id")
        id_elem.text = purchase_data.get("account_id", "")

        amount = ET.SubElement(account_amount, "amount")
        amount.text = str(purchase_data.get("amount", 0))

        fee = ET.SubElement(account_amount, "fee")
        fee.text = str(purchase_data.get("fee", 0))

        currency = ET.SubElement(account_amount, "currency")
        currency.text = str(purchase_data.get("currency", ""))

        exponent = ET.SubElement(account_amount, "exponent")
        exponent.text = str(purchase_data.get("exponent", 0))

    return ET.tostring(root, encoding="utf-8", method="xml")


def create_rp_req(
    result_code, result_desc=None,
):
    root = ET.Element("register-payment-response")

    result = ET.SubElement(root, "result")
    code = ET.SubElement(result, "code")
    code.text = str(result_code)

    if result_desc is not None:
        desc = ET.SubElement(result, "desc")
        desc.text = str(result_desc)

    return ET.tostring(root, encoding="utf-8", method="xml")


@app.route("/gpb/check-avail", methods=["GET", "POST"])
def check_avail():
    logger.info("Received request on /gpb/check-avail")
    logger.info("Request args: %s", request.args)

    # Сейчас всегда возвращается успешный ответ.
    xml_response = create_cpa_res(
        result_code=1,
        result_desc="Payment is available",
        purchase_data={
            "account_id": uuid.uuid4().hex,
            "longDesc": "test",
            "amount": "1000",
            "fee": "0",
            "currency": "643",
            "exponent": "2",
        },
    )

    is_valid, errors = validate_xml(xml_response, BASE_DIR / "schema.xsd")
    if not is_valid:
        return Response(f"Invalid XML: {errors}", status=400, mimetype="text/plain")

    return Response(xml_response, mimetype="application/xml")


@app.route("/gpb/payment-reg", methods=["GET", "POST"])
def payment_reg():
    logger.info("Received request on /gpb/payment-reg")
    logger.info("Request args: %s", request.args)

    # Сейчас всегда возвращается успешный ответ.
    xml_response = create_rp_req(
        result_code=1,
        result_desc="OK",
    )

    is_valid, errors = validate_xml(xml_response, BASE_DIR / "schema.xsd")
    if not is_valid:
        return Response(f"Invalid XML: {errors}", status=400, mimetype="text/plain")

    return Response(xml_response, mimetype="application/xml")


if __name__ == "__main__":
    logger.info("Starting Flask app...")
    app.run()
