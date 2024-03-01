package net.cpbackend.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import jakarta.persistence.*;

@JsonIgnoreProperties(ignoreUnknown = true)
@Entity
@DiscriminatorValue("M")
public class Motosega extends Attrezzo {
	
	private static final long serialVersionUID = -8361312111042952575L;
	
	@Column(name = "catena_di_taglio")
    private String catenaDiTaglio;
	
	public Motosega() {}

	public Motosega(String seriale, String marca, Stanza stanza, int potenzaWatt, String catenaDiTaglio) {
		super(seriale, marca, stanza, potenzaWatt);
		this.catenaDiTaglio = catenaDiTaglio;
	}

	public String getCatenaDiTaglio() {
		return catenaDiTaglio;
	}

	public void setCatenaDiTaglio(String catenaDiTaglio) {
		this.catenaDiTaglio = catenaDiTaglio;
	}

	@Override
	public String toString() {
		return "Motosega [catenaDiTaglio=" + catenaDiTaglio + ", toString()=" + super.toString() + "]";
	}
}
