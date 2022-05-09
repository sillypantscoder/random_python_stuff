import ui

# Initialization line
# 	ui.init(screen, font)
# You can use your own screen and font if you want.
ui.pygame.font.init()
ui.init(ui.pygame.display.set_mode([500, 500]), ui.pygame.font.SysFont("monospace", 12))

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

# ---------------------------------------------------------------------------------------------------------------------

ui.uimenu(u)
# This function will render the UI to the screen, and listen for clicks.
# It will return the index of the selected option.
# Non-clickable elements will still contribute to the index of the selected option!

ui.listmenu(lambda x: [ui.Header("Hi"), ui.Text("Hello"), ui.Option("World")])
# This function is the lowest-level way to create a menu.
# It takes a function that returns a list of UIElements.