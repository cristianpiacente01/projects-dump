package net.cpbackend.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import net.cpbackend.model.Stabilimento;

@Repository
public interface IStabilimentoRepository extends CrudRepository<Stabilimento, Long> {
}