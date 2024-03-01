package net.cpbackend.model;

import java.io.Serializable;
import java.util.Collection;
import java.util.Objects;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import jakarta.persistence.*;
import net.cpbackend.model.id.Identifiable;

@JsonIgnoreProperties(ignoreUnknown = true)
@Entity
public class Dipendente implements Serializable, Identifiable {
	
	private static final long serialVersionUID = 8648155841129531213L;

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "id_dipendente")
    private Long id;

    private String nome;

    private String cognome;

    private String mansione;

    @ManyToOne
    @JoinColumn(name = "supervisore")
    private Dipendente supervisore;

    @ManyToMany(fetch = FetchType.EAGER)
    @JoinTable(name = "haaccesso",
               joinColumns = { @JoinColumn(name = "id_dipendente") },
               inverseJoinColumns = { @JoinColumn(name = "id_stanza") }
    )
    private Collection<Stanza> stanze;

    public Dipendente() {}

	public Dipendente(String nome, String cognome, String mansione, Dipendente supervisore,
			Collection<Stanza> stanze) {
		this.nome = nome;
		this.cognome = cognome;
		this.mansione = mansione;
		this.supervisore = supervisore;
		this.stanze = stanze;
	}
	
	@Override
	public Long getId() {
		return id;
	}
	
	@Override
	public void setId(Long id) {
		this.id = id;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public String getCognome() {
		return cognome;
	}

	public void setCognome(String cognome) {
		this.cognome = cognome;
	}

	public String getMansione() {
		return mansione;
	}

	public void setMansione(String mansione) {
		this.mansione = mansione;
	}

	public Dipendente getSupervisore() {
		return supervisore;
	}

	public void setSupervisore(Dipendente supervisore) {
		this.supervisore = supervisore;
	}

	public Collection<Stanza> getStanze() {
		return stanze;
	}

	public void setStanze(Collection<Stanza> stanze) {
		this.stanze = stanze;
	}
	
	@Override
	public String toString() {
		return "Dipendente [id=" + id + ", nome=" + nome + ", cognome=" + cognome + ", mansione="
				+ mansione + ", supervisore=" + supervisore + "]";
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
		Dipendente other = (Dipendente) obj;
		return Objects.equals(id, other.id);
	}
}