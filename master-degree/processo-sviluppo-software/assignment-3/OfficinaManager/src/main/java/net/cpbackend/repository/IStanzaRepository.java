package net.cpbackend.repository;

import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

import net.cpbackend.model.Stanza;

@Repository
public interface IStanzaRepository extends CrudRepository<Stanza, Long> {
}