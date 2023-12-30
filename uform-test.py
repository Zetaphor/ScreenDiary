from PIL import Image
import torch
from uform.gen_model import VLMForCausalLM, VLMProcessor

model = VLMForCausalLM.from_pretrained("unum-cloud/uform-gen")
processor = VLMProcessor.from_pretrained("unum-cloud/uform-gen")

# prompt = "[cap] Narrate the contents of the image with precision."
prompt = "[cap] This is a screenshot from my desktop running the Firefox browser. Describe the contents of the webpage."
# prompt = "[vqa] What is the main subject of the image?"
image = Image.open("desktop.png")

inputs = processor(texts=[prompt], images=[image], return_tensors="pt")
with torch.inference_mode():
     output = model.generate(
        **inputs,
        do_sample=False,
        use_cache=True,
        max_new_tokens=128,
        eos_token_id=32001,
        pad_token_id=processor.tokenizer.pad_token_id
    )

prompt_len = inputs["input_ids"].shape[1]
decoded_text = processor.batch_decode(output[:, prompt_len:])[0]
print(decoded_text)