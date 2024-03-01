package net.cpbackend.service;

import java.util.Collection;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import net.cpbackend.model.Attrezzo;
import net.cpbackend.repository.IAttrezzoRepository;

@Service
public class AttrezzoService extends BaseCrudService<Attrezzo, IAttrezzoRepository> {

	// SEARCH OPERATION
	
	public Collection<Attrezzo> search(char tipo, int potenza, int piano) {
		if ((tipo != 'M' && tipo != 'T') || potenza < 0) {
			// if the type is not valid or the attrezzo power is negative
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
		}

		try {
			// call the repository to perform the query
			return repository.search(tipo, potenza, piano);
		} catch (Exception e) {
			throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}
}
