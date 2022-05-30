import ui

# Initialization line
# 	ui.init(screen, font)
# You can use your own screen and font if you want.
ui.pygame.font.init()
ui.init(ui.pygame.display.set_mode([500, 500], ui.pygame.RESIZABLE), ui.pygame.font.SysFont(ui.pygame.font.get_default_font(), 30))

# Alternatively, you can use the following line to use the default screen and font.
ui.autoinit()

# Example menu
# 	ui.menu(header, options)
# header is a string, options is a list of strings.
# Returns the index of the selected option.
print(ui.menu("Header", ["Option 1", "Option 2", "Option 3"]))

# ---------------------------------------------------------------------------------------------------------------------

# Creating a UI
u = ui.UI()
# This creates a new UI object.
# You can add elements to it with ui.add(element):
u.add(ui.Header("Header"))
# A Header is a UIElement that displays a string as white text against a black background.
u.add(ui.Text("Text"))
# A Text is a UIElement that displays a string as black text against a white background.
# It cannot be clicked.
u.add(ui.Option("Option"))
# Options look just like Texts, but can be clicked.
# When clicked, the option will trigger all of its click events.
u.items[-1].addclick(lambda: print("Option clicked!"))
# This line of code selects the last element in the UI,
# and adds a click event to it.
# The click event will print "Option clicked!" to the console.

# ---------------------------------------------------------------------------------------------------------------------

ui.render_ui(u)
# This function renders the UI to the screen, ONCE.
# You can call it multiple times to update the screen.
for i in range(1000):
	ui.render_ui(u)
# This loop will render the UI 1000 times, without listening for clicks.
# However, the click handler we added above will be triggered if the user clicks on the option.
# Repeatedly calling render_ui() yourself is not a good idea.

# Use this instead:
ui.uimenu(u)
# This function will render the UI to the screen, and listen for clicks.
# It will return the index of the selected option.
# Non-clickable elements will still contribute to the index of the selected option!
# In this case, the return value will be:
# 	0 - The header at the top of the screen. This can't be clicked, so this value will never be returned.
# 	1 - The text element. This one also can't be clicked, so this value will also never be returned.
# 	2 - The option element. This one can be clicked, so this value can be returned.
# 			In fact, this value will always be returned, because it's the only clickable element in the UI.

ui.listmenu(lambda x: [ui.Header("Hi"), ui.Text("Hello"), ui.Option("World").addclick(x)])
# This function is the lowest-level way to create a menu.
# It takes a function that returns a list of UIElements.
# The argument of the function is a function that exits the menu.
# The option in the example above will exit the menu when the option is clicked.

# If you want to detect which option was clicked, you can use the following code:
selected = ui.listmenu(lambda x: [ui.Header("Hi"), ui.Option("Something").addclick(lambda: x("something was clicked!")), ui.Option("Something else").addclick(lambda: x("something else was clicked!"))])
# In this example, if the user clicks on the "Something" option, then "selected" will be "something was clicked!".
# If the user clicks on the "Something else" option, then "selected" will be "something else was clicked!".
# You can use this to detect which option was clicked, and assign your own specific values to return for each option.

# ---------------------------------------------------------------------------------------------------------------------

# We can show the "selected" value in the window:
u = ui.UI()
u.add(ui.Header("Selected:"))
u.add(ui.Text(str(selected)))
u.add(ui.Button("Exit"))
ui.uimenu(u)
# By the way, a Button is a clickable element that displays a string inside a black rectangle.
# This program will show the value to the user, and exit when the user clicks on the button.

# Here are some more UI elements you can add:
u = ui.UI()
u.add(ui.Header("More UI elements"))
u.add(ui.Spacer(10))
# A Spacer is a UIElement that displays a white bar of a given height.
# This one is 10 pixels tall.
i = ui.pygame.image.load("weird.png")
u.add(ui.Image(i))
# An Image is a UIElement that displays a Surface.
# You can use any pygame.Surface object.
# You have to reference `ui.pygame` unless you specifically `import pygame` as well.
u.add(ui.Button("Exit"))
ui.uimenu(u)

# ---------------------------------------------------------------------------------------------------------------------

# The UI package includes focusable UI elements:
u = ui.UI()
u.add(ui.Header("Focusable UI elements"))
u.add(ui.KeyboardInput("Type here!"))
u.add(ui.KeyboardInput("Type more things here!", " !Teghimnoprsty"))
u.add(ui.Button("Exit"))
# A KeyboardInput is a UIElement that displays a string inside a black box.
# Click it to give it focus. Once it has focus, you can type text into it.
# Try it!
ui.uimenu(u)
# You may notice that the second KeyboardInput has a second argument.
# This is a string that controls what keys are allowed to be typed into it.
# For instance, if you wanted to only allow the user to type in digits, you could use "0123456789".

# We can now check what you typed:
text = u.items[1].text
u = ui.UI()
u.add(ui.Header("You typed:"))
u.add(ui.Text(text))
u.add(ui.Button("Exit"))
ui.uimenu(u)

# Dropdown menus are also available:
u = ui.UI()
u.add(ui.Header("Dropdown menu example"))
u.add(ui.Dropdown(["Something", "Something else", "A third thing"]))
u.add(ui.Button("Exit"))
ui.uimenu(u)
# The Dropdown is a UIElement that displays a string inside a black box.
# Clicking on the box (i.e. focusing the element) will open a menu with all the options.
# The selected option will be displayed inside the box.
# We can check which option was selected:
selected = u.items[1].getSelected()
u = ui.UI()
u.add(ui.Header("You selected:"))
u.add(ui.Text(selected))
u.add(ui.Button("Exit"))
ui.uimenu(u)
# The Dropdown class has a `getSelected()` method to get the selected option.
# The Dropdown element is new, and it doesn't support all fonts yet.
# For now, if you're using dropdown menus, you should use the font I used at the beginning.
# (It's also the default font, if you used auto_init().)

# ---------------------------------------------------------------------------------------------------------------------

# Here is an example of a menu.
# It prompts the user to create a Minecraft world, and gives the user some settings to play around with.

u = ui.UI().add(ui.Header("Create Minecraft World"))
u.add(ui.Text("Select World Name:"))
u.add(ui.KeyboardInput("world", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"))
u.add(ui.Text("Enter World Seed: (optional)"))
u.add(ui.KeyboardInput("", "0123456789-"))
u.add(ui.Text("Select Gamemode:"))
u.add(ui.Dropdown(["Survival", "Creative"]))
u.add(ui.Button("Create World >"))
valid = False
while not valid:
	ui.uimenu(u)
	w_name = u.items[2].text
	w_seed = u.items[4].text
	w_gamemode = u.items[6].options[u.items[6].selected]
	valid = True
	if w_seed != "":
		# you can have a world with no seed
		try:
			int(w_seed)
			# check if the seed is a valid number
		except:
			valid = False
	# check if world name is valid
	worldlist = ["something", "something_else"]
	if w_name in worldlist:
		valid = False
# Valid world settings, create world
u = ui.UI()
u.add(ui.Header("World Created!"))
u.add(ui.Text("World Name: " + w_name))
u.add(ui.Text("World Seed: " + w_seed))
u.add(ui.Text("Gamemode: " + w_gamemode))
u.add(ui.Button("Exit"))
ui.uimenu(u)
