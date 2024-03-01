package net.cpbackend.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import net.cpbackend.model.Dipendente;

@Repository
public interface IDipendenteRepository extends CrudRepository<Dipendente, Long> {
}
