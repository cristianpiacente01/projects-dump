package net.cpbackend.controller;

import java.util.Collection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import net.cpbackend.model.Attrezzo;
import net.cpbackend.service.AttrezzoService;

@RestController
@RequestMapping("/officina")
public class AttrezzoController {

	@Autowired
	private AttrezzoService service;

	// CREATE

	@PostMapping("/attrezzi")
	public Attrezzo create(@Validated @RequestBody Attrezzo entity) {
		return service.create(entity);
	}

	// READ

	@GetMapping("/attrezzi/{id}")
	public Attrezzo findById(@PathVariable("id") Long primaryKey) {
		return service.findById(primaryKey);
	}

	@GetMapping("/attrezzi")
	public Collection<Attrezzo> findAll() {
		return service.findAll();
	}

	// UPDATE

	@PutMapping("/attrezzi/{id}")
	public Attrezzo update(@PathVariable("id") Long primaryKey, @Validated @RequestBody Attrezzo updatedEntity) {
		return service.update(primaryKey, updatedEntity);
	}

	// DELETE

	@DeleteMapping("/attrezzi/{id}")
	public Attrezzo delete(@PathVariable("id") Long primaryKey) {
		return service.deleteById(primaryKey);
	}
	
	// SEARCH OPERATION
	
	@GetMapping("/attrezzi/search/{tipo}/{potenza}/{piano}")
	public Collection<Attrezzo> search(@PathVariable("tipo") char tipo,
								 @PathVariable("potenza") int potenza,
								 @PathVariable("piano") int piano) {
		return service.search(tipo, potenza, piano);
	}
}