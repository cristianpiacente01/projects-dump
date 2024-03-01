package net.cpbackend.service;

import java.util.Collection;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.data.repository.CrudRepository;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import net.cpbackend.model.id.Identifiable;

// abstract class used to create the concrete service classes
public abstract class BaseCrudService
	<EntityType extends Identifiable, 
	RepositoryType extends CrudRepository<EntityType, Long>> {

	@Autowired
	protected RepositoryType repository;

	// CREATE
	
	public EntityType create(EntityType entity) {
		try {
			return repository.save(entity);
		} catch (DataIntegrityViolationException e) {
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
		} catch (Exception e) {
			throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}
	
	// READ

	public EntityType findById(Long primaryKey) {
		if (primaryKey == null) {
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
		}

		Optional<EntityType> found = repository.findById(primaryKey);

		if (found.isEmpty()) {
			throw new ResponseStatusException(HttpStatus.NOT_FOUND);
		}

		return found.get();
	}

	public Collection<EntityType> findAll() {
		return (Collection<EntityType>) repository.findAll();
	}
	
	// UPDATE

	public EntityType update(Long primaryKey, EntityType updatedEntity) {
		// if the URL parameter was not passed OR the request body is empty
		// OR the entity's id was passed but it was a different id from the URL parameter
		if (primaryKey == null || updatedEntity == null || (updatedEntity.getId() != null && !primaryKey.equals(updatedEntity.getId()))) {
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
		}

		// initial checks on the passed URL parameter (e.g. a non-existent entity's id)
		findById(primaryKey);
		
		// if the entity's id was not passed, set it to the URL parameter
		updatedEntity.setId(primaryKey);

		try {
			return repository.save(updatedEntity);
		} catch (DataIntegrityViolationException e) {
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
		} catch (Exception e) {
			throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}
	
	// DELETE

	public EntityType deleteById(Long primaryKey) {
		if (primaryKey == null) {
			throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
		}

		EntityType found = findById(primaryKey);

		try {
			repository.delete(found);
			return found;
		} catch (Exception e) {
			throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}
}
