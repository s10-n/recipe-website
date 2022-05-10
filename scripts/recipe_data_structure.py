import re

recipe = {
    "recipe_name": "", #string
    "tags":["","",""], #list of strings
    "serves": "", #int
    "prep_time": "", #string
    "cook_time": "", #string
    "image_url": "", #path to image
    "recipe_description": "", #string
    "tips": "", #string
    "ingredients": ["", ["","",""],"",["","",""]], #string for subsection, list of strings for ingredients
    "directions": ["","",""], #list of strings
}

oxtail_recipe = {
    "recipe_name": "New Jamaican Oxtail Stew", #string
    "tags":["jamaican","oxtail","stew"], #list of strings
    "serves": "4", #string
    "prep_time": "12 hours", #string
    "cook_time": "4 hours", #string
    "image_url": "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fafricanbites.com%2Fwp-content%2Fuploads%2F2015%2F11%2FIMG_6154-2.jpg&f=1&nofb=1", #path to image
    "recipe_description": "Kirsten's aunt gave me this recipe, and it's my go-to for a delectable warm weather feast. I've braised pork shoulder using the same directions and it's turned out wonderfully.", #string
    "tips": "Serve with Jamaican rice and cornbread. Navy beans or butter beans can be used.", #string
    "ingredients": ["Dry rub", ["1 tbsp salt","1 tbsp allspice","1 tbsp smoked paprika"],"Stew",["3 lbs oxtail","4 tbsp butter","3 large carrots, chopped"]], #string for subsection, list of strings for ingredients
    "directions": ["Mix the dry rub ingredients in a bowl, and coat the oxtail. Once the oxtail is completely coated, dump the contents of the bowl into a plastic bag or other airtight container and refrigerate overnight.","Preheat the oven to 350. Melt the butter and olive oil in a dutch oven.","Add the oxtail and brown it on all sides. There should be a nice brown colour in the botton of the casserole dish."], #list of strings
}

def create_recipe_html(recipe_data):
    
    # open recipe template
    recipe_template_file = open("../recipes/recipe_template.html","r")

    # copy recipe template text into memory and close template
    recipe_template_text = recipe_template_file.read()
    recipe_template_file.close()
    
    # create variables from recipe data
    recipe_name = recipe_data["recipe_name"]
    tags = ""
    for tag in recipe_data["tags"]:
        tags += f"""<a href='../tags/{tag}.html'>{tag}</a>, """
    serves = recipe_data["serves"]
    prep_time = recipe_data["prep_time"]
    cook_time = recipe_data["cook_time"]
    image_url = recipe_data["image_url"]
    recipe_description = recipe_data["recipe_description"]
    tips = recipe_data["tips"]
    ingredients = ""
    for ingredient in recipe_data["ingredients"]:
        if isinstance(ingredient, str):
            ingredients += f"""<h3>{ingredient}</h3>"""
        elif isinstance(ingredient, list):
            ingredients += """<ul class="ingredient_list"</ul>"""
            for individual_ingredient in ingredient:
                ingredients += f"""<li><label><input type="checkbox">{individual_ingredient}</label></li>"""
            ingredients += "</ul>"
    directions = "<ol>"
    for step in recipe_data["directions"]:
        directions += f"""<li>{step}</li>"""
    directions += "</ol>"
    
    # replace variables in recipe template with recipe_data values
    recipe_template_text=re.sub("{recipe_name}",recipe_name,recipe_template_text)
    recipe_template_text=re.sub("{tags}",tags,recipe_template_text)
    recipe_template_text=re.sub("{serves}",serves,recipe_template_text)
    recipe_template_text=re.sub("{prep_time}",prep_time,recipe_template_text)
    recipe_template_text=re.sub("{cook_time}",cook_time,recipe_template_text)
    recipe_template_text=re.sub("{image_url}",image_url,recipe_template_text)
    recipe_template_text=re.sub("{recipe_description}",recipe_description,recipe_template_text)
    recipe_template_text=re.sub("{tips}",tips,recipe_template_text)
    recipe_template_text=re.sub("{ingredients}",ingredients,recipe_template_text)
    recipe_template_text=re.sub("{directions}",directions,recipe_template_text)

    # write the new recipe to an html file
    new_recipe_file_name = re.sub('\s', '-',f"{recipe_name}".lower()) + ".html"
    new_recipe_file = open(f"../recipes/{new_recipe_file_name}", "w")
    new_recipe_file.write(recipe_template_text)
    new_recipe_file.close()

create_recipe_html(oxtail_recipe)
