import torch 
from torch.autograd import Variable 
import torchvision.transforms as transforms
from PIL import Image , ImageOps

imgsize = 224, 224 

#PIL 이미지를 tensor 로 변경 해준다. 
def image_to_tensor(pil_image):
	# 이미지 사이지 재설정 
	resized = ImageOps.fit(pil_image , imgsize , Image.ANTIALIAS)
	# torch tensor 로 변환해준다. 
	loader = transforms.Compose([
		transforms.ToTensor()])
	return loader(resized).unsqueeze(0) 

# load model 
def load_model():
	return torch.load("finetunned_model")

# path 에 있는 이미지의 라벨을 가져 와준다. 
def is_coat(path):
	one_image = load_image(path)
	image_tensor = image_to_tensor(one_image)
	image_as_variable = Variable(image_tensor)
	model = load_model()
	model.eval()
	probabilities = model.forward(image_as_variable)
	print(probabilities)
	coat_prob = get_coat_probability(probabilities)
	print("coat probability :{}%".format(coat_prob*100))
	get_probability(probabilities)
	return coat_prob

def get_probability(all_probabilities):
	probs = all_probabilities.data.numpy()[0]
	print(probs[0])
	print(probs[1])
	print(probs[2])
	print(probs[3])
	print(probs[4])
	return "stop"

def get_coat_probability(all_probabilities):
	probs = all_probabilities.data.numpy()[0]
	index = 0
	maxValue = probs[0]
	if probs[0] > probs[1] and probs[0] > probs[2] and probs[0] > probs[3] and probs[0] > probs[4]:
		return "coat"
	if probs[2] > probs[0] and probs[2] > probs[1] and probs[2] > probs[3] and probs[2] > probs[4]:
		return "padding" 
	if probs[4] > probs[0] and probs[4] > probs[1] and probs[4] > probs[2] and probs[4] > probs[3]:
		return "short"
	if probs[3] > probs[0] and probs[3] > probs[1] and probs[3] > probs[2] and probs[3] > probs[4]:
		return "shirt"
	if probs[1] > probs[0] and probs[1] > probs[2] and probs[1] > probs[3] and probs[1] > probs[4]:
		return "hood"

	
def load_image(path):
	return Image.open(path)