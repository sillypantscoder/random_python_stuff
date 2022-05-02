def aspect_scale(img, box_width, box_height):
	""" Scales 'img' to fit into box bx/by.
	 This method will retain the original image's aspect ratio """
	image_width, image_height = img.get_size()
	if image_width > image_height:
		# fit to width
		scale_factor = box_width/float(image_width)
		scaled_height = scale_factor * image_height
		if scaled_height > box_height:
			scale_factor = box_height/float(image_height)
			scaled_width = scale_factor * image_width
			scaled_height = box_height
		else:
			scaled_width = box_width
	else:
		# fit to height
		scale_factor = box_height/float(image_height)
		scaled_width = scale_factor * image_width
		if scaled_width > box_width:
			scale_factor = box_width/float(image_width)
			scaled_width = box_width
			scaled_height = scale_factor * image_height
		else:
			scaled_height = box_height
	return (scaled_width, scaled_height)
