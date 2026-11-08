from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import ContactoForm
from .models import db, ContactMessage

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    # Muestra la landing con el formulario
    form = ContactoForm()
    return render_template("index.html", form=form)


def _compose_lead_message(form):
    parts = []
    if form.cargo.data:
        parts.append(f"Cargo: {form.cargo.data}")
    if form.tamano_empresa.data:
        parts.append(f"Tamaño empresa: {form.tamano_empresa.data}")
    if form.necesidad.data:
        label = dict(form.necesidad.choices).get(form.necesidad.data, form.necesidad.data)
        parts.append(f"Necesidad: {label}")
    if parts:
        parts.append("")
    parts.append(form.mensaje.data)
    return "\n".join(parts)


@main.route("/contacto", methods=["POST"])
def contacto():
    form = ContactoForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            nombre=form.nombre.data,
            email=form.email.data,
            telefono=form.telefono.data,
            empresa=form.empresa.data,
            mensaje=_compose_lead_message(form),
        )
        db.session.add(msg)
        db.session.commit()
        flash("Gracias. Un especialista de Stratechic revisará tu desafío y se pondrá en contacto contigo.", "success")

        # Redirige a la misma página donde se envió el form
        next_page = request.referrer or url_for("main.index")
        return redirect(next_page + "#contacto")

    print(form.errors)
    flash("Hay errores en el formulario. Revisa los campos e inténtalo de nuevo.", "danger")
    return render_template("index.html", form=form), 400
