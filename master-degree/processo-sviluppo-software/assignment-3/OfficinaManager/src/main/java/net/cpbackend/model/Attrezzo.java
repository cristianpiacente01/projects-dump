package net.cpbackend.model;

import java.io.Serializable;
import java.util.Objects;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import jakarta.persistence.*;
import net.cpbackend.model.id.Identifiable;

/*
 * Every entity has a Long PK and it gets generated
 * using the strategy GenerationType.IDENTITY
 * (to exploit the AUTO_INCREMENT of MySQL).
 * 
 * An entity implements the interface Identifiable
 * to have a common getter and a common setter of the ID
 * and so the same signature for each class.
 * 
 * Regarding Attrezzo, the strategy SINGLE_TABLE was used
 * to map the inheritance, so there's only 1 table in the DB
 * that maps all the classes of the same hierarchy: 
 * the reason behind this choice is that there's only 1 NULL value
 * for each record (tipo_di_punta for Motosega and
 * catena_di_taglio for Trapano).
 * 
 * The annotation @JsonIgnoreProperties was added for testing purposes,
 * to always obtain a ResponseEntity even when the response was not successful.
 */

@JsonIgnoreProperties(ignoreUnknown = true)
@Entity
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "tipo", discriminatorType = DiscriminatorType.CHAR)
@DiscriminatorValue("A") // safe
public abstract class Attrezzo implements Serializable, Identifiable {

	private static final long serialVersionUID = 514754107803193884L;

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "id_attrezzo")
	protected Long id;

	protected String modello;

	protected String marca;

	@ManyToOne
	@JoinColumn(name = "id_stanza")
	protected Stanza stanza;
	
	@Column(insertable = false, updatable = false)
	private char tipo;

	@Column(name = "potenza_watt")
	protected int potenzaWatt;

	protected Attrezzo() {
		// initialize tipo
		this.tipo = this.getClass().getAnnotation(DiscriminatorValue.class).value().charAt(0);
	}

	protected Attrezzo(String modello, String marca, Stanza stanza, int potenzaWatt) {
		this(); // set up the type
		
		this.modello = modello;
		this.marca = marca;
		this.stanza = stanza;
		this.potenzaWatt = potenzaWatt;
	}

	@Override
	public Long getId() {
		return id;
	}

	@Override
	public void setId(Long id) {
		this.id = id;
	}

	public String getModello() {
		return modello;
	}

	public void setModello(String modello) {
		this.modello = modello;
	}

	public String getMarca() {
		return marca;
	}

	public void setMarca(String marca) {
		this.marca = marca;
	}

	public Stanza getStanza() {
		return stanza;
	}

	public void setStanza(Stanza stanza) {
		this.stanza = stanza;
	}

	public int getPotenzaWatt() {
		return potenzaWatt;
	}

	public void setPotenzaWatt(int potenzaWatt) {
		this.potenzaWatt = potenzaWatt;
	}
	
	public char getTipo() {
		return tipo;
	}

	@Override
	public String toString() {
		return "Attrezzo [id=" + id + ", modello=" + modello + ", marca=" + marca + ", stanza=" + stanza
				+ ", potenzaWatt=" + potenzaWatt + "]";
	}

	@Override
	public int hashCode() {
		return Objects.hash(id);
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Attrezzo other = (Attrezzo) obj;
		return Objects.equals(id, other.id);
	}
}
