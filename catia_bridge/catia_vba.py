import win32com.client

def run_catia_vba():
    catia = win32com.client.Dispatch("CATIA.Application")
    documents = catia.Documents
    file_path = "C:\\Users\\Ken\\Documents\\Product1.CATProduct"
    document_name = "Product1.CATProduct"
    try:
        document = documents.Item(document_name)
    except:
        document = documents.Open(file_path)

    # Assumes that the VBA script is already available in Catia
    catia.SystemService.ExecuteScript(
        # Macro library name/path
        r"E:\Dev\PythonScripts\catia_bridge\vbscripts",
        # Type of macro library (document/directory/VBA project)
        1,
        # Macro name
        "bridge.catvbs",
        # Function name
        "CATMain",
        #Arguments
        tuple()
    )

if __name__ == "__main__":
    run_catia_vba()