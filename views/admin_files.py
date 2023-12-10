from common.common_functions import ManagePDF, ReturnJsonRequest

def upload_file(request):
    admin_pdf_file = ManagePDF(request)
    admin_pdf_file.save_temp_file()
    admin_pdf_file.reading_pdf()
    admin_pdf_file.clean_json_file()
    admin_pdf_file.save_json_texts_list()
    admin_pdf_file.remove_temp_file()
    return_format = ReturnJsonRequest()
    return return_format.json_return_format(200, "File uploaded successfully")
