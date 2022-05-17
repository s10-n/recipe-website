import re
import os
from bs4 import BeautifulSoup
import recipe_data_structure




# What happens when a new recipe is submitted?

# create a new HTML page with the recipe data in the /recipes directory

def create_recipe_html(recipe_data): # create new HTML page
    
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
    tags = tags[:-2]
    serves = recipe_data["serves"]
    prep_time = recipe_data["prep_time"]
    cook_time = recipe_data["cook_time"]
    if "image_url" in recipe_data:
        image_url = recipe_data["image_url"]
    else:
        image_url = ''
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
    if image_url: # check if there is an image
        recipe_template_text=re.sub("{image_url}",image_url,recipe_template_text)
    else:
        recipe_template_text=re.sub("""<img id="image" src="{image_url}">""",image_url,recipe_template_text)
    recipe_template_text=re.sub("{recipe_description}",recipe_description,recipe_template_text)
    if tips: # check if there are tips
        recipe_template_text=re.sub("{tips}",tips,recipe_template_text)
    else:
        recipe_template_text=re.sub("""<section id="tips">
	  <h3>Tips</h3>
	  <p>{tips}</p>
	</section>""",tips,recipe_template_text)
    recipe_template_text=re.sub("{ingredients}",ingredients,recipe_template_text)
    recipe_template_text=re.sub("{directions}",directions,recipe_template_text)

    # write the new recipe to an html file
    new_recipe_file_name = re.sub('\s', '-',f"{recipe_name}".lower()) + ".html"
    new_recipe_file = open(f"../recipes/{new_recipe_file_name}", "w")
    new_recipe_file.write(recipe_template_text)
    print(f'Wrote {recipe_name} to {new_recipe_file_name}')
    new_recipe_file.close()

# update index.html by adding a link to the new recipe under the correct header in relative alphabetical order

def rewrite_index():
    # open index.html
    index_page = open("../index_template.html","r")
    soup = BeautifulSoup(index_page, 'html.parser')
    index_page.close()
    # open recipe list
    recipe_list = sorted(recipe_data_structure.recipes, key=lambda item:item.get("recipe_name"))
    
    # iterate through all recipes in the recipe list
    for recipe in recipe_list:
        # get the first letter of each recipe
        recipe_name = recipe["recipe_name"]
        recipe_link = re.sub('\s', '-',f"recipes/{recipe_name}".lower()) + ".html"
        first_letter = recipe_name[0].lower()

        # find the correct subsection for the recipe
        navigation_section = soup.find(id=f"{first_letter}")

        # create a new list item for the recipe
        recipe_li = soup.new_tag('li')
        recipe_a = soup.new_tag('a')
        recipe_a["href"] = recipe_link
        recipe_a.string = recipe_name
        recipe_li.append(recipe_a)

        # add the new list item to the index page
        navigation_section.append(recipe_li)
        print(f'Added {recipe_name} to index page')

        # update tags on index page

        # get the recipe's tags
        tags = recipe["tags"]

        # open the tag cloud element for the index page
        tag_cloud = soup.find(id="tag_cloud")

        # for each tag, add it to the tag cloud
        for tag in tags:
            if not tag_cloud.find(string=tag):
                tag_a = soup.new_tag('a')
                tag_a["href"] = "tags/" + tag + ".html"
                tag_a.string = tag
                tag_a.append(", ")
                tag_cloud.append(tag_a)

        # create a page for the recipe
        create_recipe_html(recipe)

    # sort tags alphabetically
    tag_links = tag_cloud.find_all('a')
    sorted_tag_links = sorted(tag_links, key=lambda elem: elem.text)

    # add the sorted tags to the index page
    for i in sorted_tag_links:
        tag_cloud.append(i)

    # remove last comma from tag cloud
    last_tag = tag_cloud.find_all()[-1].contents
    
    
    tag_cloud.find_all()[-1].string = last_tag[0]
    index_page = open("../index.html","w")
    index_page.write(str(soup))
    index_page.close()      
rewrite_index()



# for each tag associated with the recipe:
# if a tag page exists, add the recipe to the tag page in relative alphabetical order
# if a tag page doesn't exist, create it and add the recipe to it

# for any new tag pages created, update index.html and add them to the tag cloud
