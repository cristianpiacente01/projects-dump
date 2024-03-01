package net.cpbackend.model;

import java.io.Serializable;
import java.util.Objects;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import jakarta.persistence.*;
import net.cpbackend.model.id.Identifiable;

@JsonIgnoreProperties(ignoreUnknown = true)
@Entity
public class Stabilimento implements Serializable, Identifiable {
	
	private static final long serialVersionUID = 2625458761990731383L;

	@Id 
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "id_stabilimento")
	private Long id;
	
	private String nome;
	
	public Stabilimento() {}
	
	public Stabilimento(String nome) {
		this.nome = nome;
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

	@Override
	public String toString() {
		return "Stabilimento [id=" + id + ", nome=" + nome + "]";
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
		Stabilimento other = (Stabilimento) obj;
		return Objects.equals(id, other.id);
	}
}
