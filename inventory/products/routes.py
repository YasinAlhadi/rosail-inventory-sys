#!/usr/bin/python3
"""This module contains the products routes"""
from flask import Blueprint, render_template, url_for, flash, redirect, request
from inventory.models.product import Product, Category, Brand
from inventory.products.forms import ProductForm, CategoryForm, BrandForm
from inventory import db
from flask_login import login_required, current_user

prod = Blueprint('products', __name__)

@prod.route('/products')
def products():
    """This function defines the products route"""
    products = Product.query.all()

    user = current_user
    return render_template('products.html', title='Products', products=products, user=user)

@prod.route('/products/new', methods=['GET', 'POST'])
def new_product():
    """This function defines the new product route"""
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, price=form.price.data, quantity=form.quantity.data, category_id=form.category.data, brand_id=form.brand.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('products.products'))
    categories = Category.query.all()
    brands = Brand.query.all()
    user = current_user
    return render_template('add_product.html', title='New Product', categories=categories, brands=brands, form=form, user=user)

@prod.route('/products/<int:product_id>/update', methods=['GET', 'POST'])
def update_product(product_id):
    """This function defines the update product route"""
    product = Product.query.get_or_404(product_id)
    user = current_user
    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.category_id = form.category.data
        product.brand_id = form.brand.data
        product.description = form.description.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products.product', product_id=product.id))
    elif request.method == 'GET':
        form.name.data = product.name
        form.price.data = product.price
        form.quantity.data = product.quantity
        form.category.data = product.category_id
        form.brand.data = product.brand_id
        form.description.data = product.description
    categories = Category.query.all()
    brands = Brand.query.all()
    return render_template('update_product.html', title='Update Product', categories=categories, brands=brands, form=form, user=user)

@prod.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    """This function defines the delete product route"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products.products'))

@prod.route('/categories')
def categories():
    """This function defines the categories route"""
    categories = Category.query.all()
    user = current_user
    return render_template('categories.html', title='Categories', categories=categories, user=user)

@prod.route('/categories/new', methods=['GET', 'POST'])
def new_category():
    """This function defines the new category route"""
    user = current_user
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, description=form.description.data)
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('products.categories'))
    return render_template('add_category.html', title='New Category', form=form, user=user)


@prod.route('/categories/<int:category_id>/update', methods=['GET', 'POST'])
def update_category(category_id):
    """This function defines the update category route"""
    category = Category.query.get_or_404(category_id)
    user = current_user
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('products.category', category_id=category.id))
    elif request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
    return render_template('update_category.html', title='Update Category', form=form , user=user)

@prod.route('/categories/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    """This function defines the delete category route"""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('products.categories'))

@prod.route('/brands')
def brands():
    """This function defines the brands route"""
    brands = Brand.query.all()
    user = current_user
    return render_template('brands.html', title='Brands', brands=brands, user=user)

@prod.route('/brands/new', methods=['GET', 'POST'])
def new_brand():
    """This function defines the new brand route"""
    form = BrandForm()
    if form.validate_on_submit():
        brand = Brand(name=form.name.data, description=form.description.data)
        db.session.add(brand)
        db.session.commit()
        flash('Brand created successfully!', 'success')
        return redirect(url_for('products.brands'))
    user = current_user
    return render_template('add_brand.html', title='New Brand', form=form, user=user)

@prod.route('/brands/<int:brand_id>/update', methods=['GET', 'POST'])
def update_brand(brand_id):
    """This function defines the update brand route"""
    brand = Brand.query.get_or_404(brand_id)
    user = current_user
    form = BrandForm()
    if form.validate_on_submit():
        brand.name = form.name.data
        brand.description = form.description.data
        db.session.commit()
        flash('Brand updated successfully!', 'success')
        return redirect(url_for('products.brands', brand_id=brand))
    elif request.method == 'GET':
        form.name.data = brand.name
        form.description.data = brand.description
    return render_template('update_brand.html', title='Update Brand', form=form, user=user)

@prod.route('/brands/<int:brand_id>/delete', methods=['POST'])
def delete_brand(brand_id):
    """This function defines the delete brand route"""
    brand = Brand.query.get_or_404(brand_id)
    if brand.products:
        flash('Brand has products associated with it. Delete products first!', 'danger')
        return redirect(url_for('products.brands'))
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        flash('Brand deleted successfully!', 'success')
        return redirect(url_for('products.brands'))