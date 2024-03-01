package net.cpbackend.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import jakarta.persistence.*;

@JsonIgnoreProperties(ignoreUnknown = true)
@Entity
@DiscriminatorValue("T")
public class Trapano extends Attrezzo {
	
	private static final long serialVersionUID = -8192824985547834481L;
	
	@Column(name = "tipo_di_punta")
    private String tipoDiPunta;
	
	public Trapano() {}

	public Trapano(String seriale, String marca, Stanza stanza, int potenzaWatt, String tipoDiPunta) {
		super(seriale, marca, stanza, potenzaWatt);
		this.tipoDiPunta = tipoDiPunta;
	}

	public String getTipoDiPunta() {
		return tipoDiPunta;
	}

	public void setTipoDiPunta(String tipoDiPunta) {
		this.tipoDiPunta = tipoDiPunta;
	}

	@Override
	public String toString() {
		return "Trapano [tipoDiPunta=" + tipoDiPunta + ", toString()=" + super.toString() + "]";
	}
}
