from django.shortcuts import render

def safe_text(text):
    text = text.replace("\r","")
    text = text.replace("\n","")
    text = text.replace('"',"'")
    text = text.replace("\\","\\\\")
    return text

def editor(request,submit_url,serialized_form_data,header,initial_text):
    # Make sure we strip out all escape characters
    initial_text = safe_text(initial_text)
    context={'submit_url':submit_url, \
             'serialized_form_data':serialized_form_data, \
             'header':header, \
             'initial_text':initial_text, \
            }
    return render(request, 'MCEditor/editor.html', context)
