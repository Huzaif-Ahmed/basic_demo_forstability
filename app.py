
from flask import Flask, render_template, request, jsonify
import replicate
import openai

app = Flask(__name__, static_folder='static')








@app.route('/')
def index():
    return render_template('index.html')



@app.route('/process_input', methods=['POST'])
def process_input():
    message = request.form.get('message')

    if message:
        openai.api_key ="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"
        messages = [
            {"role": "system", "content": "act as a prompt engineer and your job is to act as a translator between the user and the stable-diffusion model .a user will be giving you input that describes an attire or a dress, and you need to use your imagination, creative skills to make a prompt which describes a photo which consists view, attire, and the scenery, also do mention the body physique features of the fashion model wearing the dress for the picture to look more appealing and attractive and also make the fashion model and scenery bright such that user should get attracted to buy that dress. don't use words like imagine and etc,just give a title for that image give description and dont make the prompt too descriptive make it in 100  words but very informative.do not remove the features of description from the input just add your creativity.DO NOT GENERATE INPUT ON YOUR OWN WAIT FOR THE USER TO PROVIDE INPUT AND THEN MAKE A PROMPT"},
        ]

        
        if message:
            messages.append(
                {"role": "user", "content": message},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )

        reply = chat.choices[0].message.content
        print(f"ChatGPT: {reply}")




        output = replicate.run(
            "stability-ai/sdxl:a00d0b7dcbb9c3fbb34ba87d2d5b46c56969c84a628bf778a7fdaec30b1b99c5",
            input={"prompt": reply}
        )

        
        output_image_url = output[0]

        return jsonify({"output": output_image_url})

    return jsonify({"error": "Missing 'message' in form data."})

if __name__ == "__main__":
    app.run(debug=True)


