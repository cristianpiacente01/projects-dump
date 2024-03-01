package net.cpbackend.service;

import org.springframework.stereotype.Service;

import net.cpbackend.model.Dipendente;
import net.cpbackend.repository.IDipendenteRepository;

@Service
public class DipendenteService extends BaseCrudService<Dipendente, IDipendenteRepository> {
}