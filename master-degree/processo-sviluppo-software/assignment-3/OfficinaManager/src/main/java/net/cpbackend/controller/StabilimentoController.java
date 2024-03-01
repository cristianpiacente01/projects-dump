package net.cpbackend.controller;

import java.util.Collection;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import net.cpbackend.model.Stabilimento;
import net.cpbackend.service.StabilimentoService;

@RestController
@RequestMapping("/officina")
public class StabilimentoController {

	@Autowired
	private StabilimentoService service;

	// CREATE

	@PostMapping("/stabilimenti")
	public Stabilimento create(@Validated @RequestBody Stabilimento entity) {
		return service.create(entity);
	}

	// READ

	@GetMapping("/stabilimenti/{id}")
	public Stabilimento findById(@PathVariable("id") Long primaryKey) {
		return service.findById(primaryKey);
	}

	@GetMapping("/stabilimenti")
	public Collection<Stabilimento> findAll() {
		return service.findAll();
	}

	// UPDATE

	@PutMapping("/stabilimenti/{id}")
	public Stabilimento update(@PathVariable("id") Long primaryKey,
			@Validated @RequestBody Stabilimento updatedEntity) {
		return service.update(primaryKey, updatedEntity);
	}

	// DELETE

	@DeleteMapping("/stabilimenti/{id}")
	public Stabilimento delete(@PathVariable("id") Long primaryKey) {
		return service.deleteById(primaryKey);
	}
}
