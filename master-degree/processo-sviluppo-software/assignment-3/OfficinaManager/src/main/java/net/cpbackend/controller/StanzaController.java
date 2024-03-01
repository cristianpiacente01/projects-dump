package net.cpbackend.controller;

import java.util.Collection;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import net.cpbackend.model.Stanza;
import net.cpbackend.service.StanzaService;

@RestController
@RequestMapping("/officina")
public class StanzaController {

	@Autowired
	private StanzaService service;

	// CREATE

	@PostMapping("/stanze")
	public Stanza create(@Validated @RequestBody Stanza entity) {
		return service.create(entity);
	}

	// READ

	@GetMapping("/stanze/{id}")
	public Stanza findById(@PathVariable("id") Long primaryKey) {
		return service.findById(primaryKey);
	}

	@GetMapping("/stanze")
	public Collection<Stanza> findAll() {
		return service.findAll();
	}

	// UPDATE

	@PutMapping("/stanze/{id}")
	public Stanza update(@PathVariable("id") Long primaryKey, @Validated @RequestBody Stanza updatedEntity) {
		return service.update(primaryKey, updatedEntity);
	}

	// DELETE

	@DeleteMapping("/stanze/{id}")
	public Stanza delete(@PathVariable("id") Long primaryKey) {
		return service.deleteById(primaryKey);
	}
}
