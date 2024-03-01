package net.cpbackend.repository;

import java.util.Collection;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import net.cpbackend.model.Attrezzo;

@Repository
public interface IAttrezzoRepository extends CrudRepository<Attrezzo, Long> {
	
	// JPQL query to implement the search operation between attrezzo and stanza
	@Query("SELECT a FROM Attrezzo a "
	        + "JOIN a.stanza s "
	        + "WHERE a.tipo = ?1 "
	        + "AND a.potenzaWatt >= ?2 "
	        + "AND s.piano = ?3")
	public Collection<Attrezzo> search(char tipo, int potenza, int piano);
}
