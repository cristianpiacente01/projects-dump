package net.cpbackend.model;

import java.io.Serializable;
import java.util.Objects;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import jakarta.persistence.*;
import net.cpbackend.model.id.Identifiable;

@JsonIgnoreProperties(ignoreUnknown = true)
@Entity
public class Stanza implements Serializable, Identifiable {	
	
	private static final long serialVersionUID = -1785048300667714957L;

	@Id 
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "id_stanza")
	protected Long id;
	
	@ManyToOne
	@JoinColumn(name = "id_stabilimento")
	private Stabilimento stabilimento;
	
	private String nome;
	
	@Column(name = "capienza_persone")
	private int capienza;
	
	private int piano;
	
	public Stanza() {}
	
	public Stanza(Stabilimento stabilimento, String nome, int capienza, int piano) {
		this.stabilimento = stabilimento;
		this.nome = nome;
		this.capienza = capienza;
		this.piano = piano;
	}
	
	@Override
	public Long getId() {
		return id;
	}
	
	@Override
	public void setId(Long id) {
		this.id = id;
	}

	public Stabilimento getStabilimento() {
		return stabilimento;
	}

	public void setStabilimento(Stabilimento stabilimento) {
		this.stabilimento = stabilimento;
	}

	public String getNome() {
		return nome;
	}

	public void setNome(String nome) {
		this.nome = nome;
	}

	public int getCapienza() {
		return capienza;
	}

	public void setCapienza(int capienza) {
		this.capienza = capienza;
	}

	public int getPiano() {
		return piano;
	}

	public void setPiano(int piano) {
		this.piano = piano;
	}

	@Override
	public String toString() {
		return "Stanza [id=" + id + ", stabilimento=" + stabilimento + ", nome=" + nome + ", capienza="
				+ capienza + ", piano=" + piano + "]";
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
		Stanza other = (Stanza) obj;
		return Objects.equals(id, other.id);
	}
}
