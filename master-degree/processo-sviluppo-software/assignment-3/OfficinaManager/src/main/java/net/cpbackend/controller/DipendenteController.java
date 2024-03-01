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

import net.cpbackend.model.Dipendente;
import net.cpbackend.service.DipendenteService;

@RestController
@RequestMapping("/officina")
public class DipendenteController {

	@Autowired
	private DipendenteService service;

	// CREATE

	@PostMapping("/dipendenti")
	public Dipendente create(@Validated @RequestBody Dipendente entity) {
		return service.create(entity);
	}

	// READ

	@GetMapping("/dipendenti/{id}")
	public Dipendente findById(@PathVariable("id") Long primaryKey) {
		return service.findById(primaryKey);
	}

	@GetMapping("/dipendenti")
	public Collection<Dipendente> findAll() {
		return service.findAll();
	}

	// UPDATE

	@PutMapping("/dipendenti/{id}")
	public Dipendente update(@PathVariable("id") Long primaryKey, @Validated @RequestBody Dipendente updatedEntity) {
		return service.update(primaryKey, updatedEntity);
	}

	// DELETE

	@DeleteMapping("/dipendenti/{id}")
	public Dipendente delete(@PathVariable("id") Long primaryKey) {
		return service.deleteById(primaryKey);
	}
}